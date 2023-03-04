from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'description', 'price', 'image', 'end_time')

    end_time = forms.DateTimeField(
        label='終了日時',#フォームに表示されるフィールド名
        input_formats=['%Y/%m/%d %H:%M'],#ユーザーの入力形式の指定
        widget=forms.DateTimeInput(attrs={#フォームの表示形式を指定,datetime-localで日付と時刻を分ける
            'type': 'datetime-local'
        })
    )
