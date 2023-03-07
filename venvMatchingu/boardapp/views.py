from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login
from .models import boardmodel
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import logout
from .models import Product
from django.shortcuts import render, redirect
from .models import Product
from .forms import ProductForm
from django.views.generic import ListView
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponseRedirect

# views.py

from boardapp.task import auction_end_check


from boardapp.task import auction_end_check
from django.http import HttpResponse


def my_view(request):
    result = auction_end_check.delay()
    # ... 他の処理 ...
    return HttpResponse("Task started")


@login_required # ログインが必要なので、ログインしていない場合はログイン画面にリダイレクトされる
def bid(request, pk):
    product = get_object_or_404(Product, pk=pk) # pkに一致するProductオブジェクトを取得、存在しなければ404エラーを返す
    if request.method == 'POST':
        bid_price = int(request.POST['bid_price']) # フォームから送信された入札価格を取得
        if bid_price > product.price: # 入札価格が現在の価格を上回っている場合
            # Bidオブジェクトを作成して保存
            product.buyer = request.user
            product.price = bid_price # 入札価格を現在の価格に更新
            product.save()
        return redirect(reverse('auction:detail', args=(pk,))) # 詳細画面にリダイレクト
    return redirect('auction:index') # POSTでなければ、トップページにリダイレクト


#class Productlist(ListView):#出品物を全て表示する
#    template_name = 'Productlist.html'
#    model = Product

class Productlist(ListView):#listviewは全ての指定モデルのオブジェクトを得る

#継承元listviewの実行順
#setup(): Viewの初期化を行う
#dispatch(): リクエストを処理するHTTPメソッドに基づいて適切なメソッドを呼び出す
#http_method_not_allowed(): dispatch()が許可されていないHTTPメソッドを受信した場合に呼び出される
#get_template_names(): テンプレート名を返す
#get_queryset(): クエリセットを返す
#get_context_object_name(): コンテキスト変数の名前を返す
#get_context_data(): テンプレートに渡すコンテキストを返す
#get(): HTTP GETメソッドでリクエストされた場合に呼び出される
#render_to_response(): HttpResponseを返す


    model = Product
    template_name = "productlist.html"
    paginate_by = 5#ページネーション、１ページにオブジェクトを5件ずつ表示する

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # 検索ワードがある場合は絞り込み
        search_word = self.request.GET.get('search_name', '')
        if search_word:
            queryset = queryset.filter(name__contains=search_word)
    
        # ソートオプションがある場合は並び替え
        sort_option = self.request.GET.get('my_select', '')
        if sort_option == 'option2':
            queryset = queryset.order_by('price')
        elif sort_option == 'option3':
            queryset = queryset.order_by('-price')
    
        return queryset


    def get_context_data(self, **kwargs):
        # 親クラスのget_context_data()を呼び出す
        context = super().get_context_data(**kwargs)
        # 検索フォームの初期値として、前回の検索語を渡す
        context['search_name'] = self.request.GET.get('search', '')
        # contextを返す
        return context







@login_required
def productcreate(request):#ユーザーが出品できるようにする
    print("product_createが実行されました")
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():#バリデーションチェックがokなら
            product = form.save(commit=False)
            product.user = request.user#登録しているユーザー名を渡す
            product.save()
            return redirect('product_detail', slug=product.slug)#スラグを渡す
        else:
            print("バリデーションチェックが失敗しました")
    else:
        form = ProductForm()#getの時、空のフォームを表示
    return render(request, 'product_create.html', {'form': form})

def product_detail(request, slug):#商品の詳細情報,product_create成功時の遷移先,入札処理も行う
    product = get_object_or_404(Product, slug=slug)
    if request.method == 'POST':
        print("入札ボタンが押されました")
        bid_price = request.POST.get('bid_price')
        time_over = request.POST.get('time_over')
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/product/{}/?success={}'.format(slug, "ログイン無しでは入札できません"))
        if request.user.username == product.user.username:
            return HttpResponseRedirect('/product/{}/?success={}'.format(slug, "出品者は入札できません"))
        if str(request.user.username) == str(product.highest_bidder):
            return HttpResponseRedirect('/product/{}/?success={}'.format(slug, "最高入札者は入札できません"))
        if time_over == "false":
            print("入札可能です")
            if float(bid_price) > product.price:# 入札価格が商品価格を上回っている場合
                print("入札できました")
                # 入札を保存
                # 商品の価格を更新
                product.price = float(bid_price)
                #最高入札者を更新
                product.highest_bidder=request.user
                product.save()
                # 入札者一覧を追加
                product.buyers.add(request.user)

                return HttpResponseRedirect('/product/{}/?success={}'.format(slug, "入札が完了しました"))

            else:
                # 入札価格が商品価格以下の場合
                print("入札価格が商品価格以下です")
                return HttpResponseRedirect('/product/{}/?success={}'.format(slug, "入札価格が商品の価格より少ないです"))
        else:
            print("オークションは終了しています")
            return HttpResponseRedirect('/product/{}/?success={}'.format(slug, "オークションは終了しています"))
    else:
        print("product_detailがgetで実行されました")
        return render(request, 'product_detail.html', {'product': product})



@login_required
def user_products(request, user_id):#ログインしているユーザーの商品情報,未ログイン時の遷移先はsettings.login
    print("user_productsが呼び出されました")
    products = Product.objects.filter(user_id=user_id)#productモデルのuseridが一致しているもののみ取り出す
    context = {
        'products': products
    }
    return render(request, 'user_products.html', context)
    
    
@login_required
def user_nyusatu_products(request, user_id):
    products = Product.objects.filter(buyers=request.user)
    context = {
        'products': products
    }
    return render(request, 'user_nyusatu.html', context)


def signupfunc(request):#新規会員登録

    print("signupfuncが呼び出されました")
    
    object_list = User.objects.all()
    object_list_detail = User.objects.get(username="yasutaka")
    
    #print("登録済みの全体のオブジェクトです",object_list)#全体のオブジェクトです <QuerySet [<User: yasutaka>, <User: sorn>]>
    #print("登録済み個別のオブジェクトです",object_list_detail,object_list_detail.email)#個別のオブジェクトです yasutaka am12012000@gmail.com
    

    #request.methodの説明
    #djangoはリクエストを受けたときにrequest.methodに情報を格納する（post,getなどの値をふくむ）
    if request.method == 'POST':
        
        print("フォームの入力値です",request.POST)
        
        #request.postでフォームの情報を受け取る
        username = request.POST['username']
        password = request.POST['password']
        #例外処理でusernameの重複を防ぐ
        try:
            
            #create_user関数でuserを作成する,この関数実行時点でデータベースにデータが保存される。
            user = User.objects.create_user(username,"" , password)
            print("作成が完了しました")
            return redirect('list')
            #必要であればこの後にuser.last_name="tanaka"の後に
            #user.save()で上書きも可能

        except IntegrityError:#integrity_errorはデータベースの一意性に違反した時などに返されるエラー
        
            print("重複しています")
            #htmlにエラー情報を渡す
            return render(request, 'signup.html', {'error': 'ユーザー名が重複しています。'})
    else:#not post
        print("this is not post")
        

    
    
    #redirectは指定したurlに遷移する、renderは指定したhtmlファイルを利用して描画を行うだけでページは遷移しない
    #return redirect("login")
    
    return render(request, 'signup.html')
    




def loginfunc(request):#ログイン処理
    print("loginfuncが呼び出されました")

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
    
        #authenticate関数で与えられたユーザネームとパスワードの組み合わせがあるか検証し、あれば、userオブジェクトをなければnoneを返す
        #login関数自体には未登録のユーザーを弾く機能がないので事前にauthenticateで検証する
        user = authenticate(request, username=username, password=password)
    
        if user is not None:

            login(request, user)
            return redirect("Productlist")
        else:

            return render(request,"login.html",{"context":"login失敗"})

    else:#not post
        return render(request,"login.html",{"context":""})

#@login_required#デコレーター指示、ログイン確認を関数実行前に実施する設定
def productlist(request):
    print("productlistがよび出されました")
    
def listfunc(request):#リストを表示する

    print("listfuncが呼び出されました？？？？？")
    object_list = boardmodel.objects.all()
    return render(request, 'list.html',{'object_list':object_list})
    


def logoutfunc(request): # ログアウト処理
   
    print("logoutfuncがよび出されました!!")
    logout(request)
    return redirect("login")
    
def detailfunc(request,pk):#個々のデータを表示する
    print("detailfuncが呼び出されました")
    #対象のオブジェクトがあればそれを返す、なければ404エラーを返す
    object = get_object_or_404(boardmodel,pk=pk)
    return render(request,'detail.html',{'object':object})

def goodfunc(request,pk):
    print("goodfuncが呼び出されました")
    #対象のオブジェクトを返す
    object = boardmodel.objects.get(pk=pk)
    object.good = object.good + 1
    object.save()
    return redirect("list")
    
def readfunc(request,pk):
    print("readfuncが呼び出されました")
    #対象のオブジェクトを返す
    object = boardmodel.objects.get(pk=pk)
    #ログインしているユーザーの情報を返す
    username=request.user.get_username()
    if username in object.readtext:#現在のログインユーザーがreadtextに登録されていれば
        return redirect('list')
    else:
        object.readtext = object.readtext+"| |"+username
        object.read = object.read + 1
        object.save()
        return redirect("list")
class boardcreate(CreateView):
    print("boardcreateがよび出されました!？？？")
    template_name="create.html"
    model = boardmodel
    fields =("title","content","author","snsimage")

    #登録後の遷移ページ
    success_url = reverse_lazy("list")
    
    
