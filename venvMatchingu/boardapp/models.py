from django.db import models
from .models import *
from django.contrib.auth.models import User
import datetime
import time
from django.utils.text import slugify

# Create your models here.

class   boardmodel(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.CharField(max_length=50)
    snsimage = models.ImageField(upload_to='')#アップロード画像の保存先、settingslotfileで設定した場所をルートとしたディレクトリを指定
    good = models.IntegerField(default=0,blank=True,null=True)
    read = models.IntegerField(default=0,blank=True,null=True)
    readtext=models.TextField(null=True,blank=True,default="a")#null=Trueはデータが空でもok,Blank=Trueはフォームが空欄でもok
    #メンバ変数title等を参照し、データの表示名を決める
    def __str__(self):
        return self.title


class   boardmodel(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.CharField(max_length=50)
    snsimage = models.ImageField(upload_to='')#アップロード画像の保存先、settingslotfileで設定した場所をルートとしたディレクトリを指定
    good = models.IntegerField(default=0,blank=True,null=True)
    read = models.IntegerField(default=0,blank=True,null=True)
    readtext=models.TextField(null=True,blank=True,default="a")#null=Trueはデータが空でもok,Blank=Trueはフォームが空欄でもok
    #メンバ変数title等を参照し、データの表示名を決める
    def __str__(self):
        return self.title


class Product(models.Model):
    name = models.CharField(max_length=255, unique=False)
    description = models.TextField(unique=False)
    price = models.PositiveIntegerField(unique=False)
    end_time = models.DateTimeField(null=True, blank=True, unique=False)
    image = models.ImageField(default="no_image.jpeg", upload_to='product_images', null=True, blank=True, unique=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(unique=False)
    bid_name = models.CharField(max_length=255, null=True, blank=True, unique=False)
    buyer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='bought_products')
    sold = models.BooleanField(default=False,null=True, blank=True, unique=False)

    def save(self, *args, **kwargs):#一意のスラグを作成する
        if not self.pk:#新しいオブジェクトが作成された時のみスラグを生成
            self.slug = orig = slugify("Product" + self.name)
            count = 0
            while Product.objects.filter(slug=self.slug).exists():
                count += 1
                self.slug = '%s-%d' % (orig, count)
        super().save(*args, **kwargs)

        
        
        
class Product2(models.Model):#商品データを扱う
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.PositiveIntegerField()
    end_time = models.DateTimeField(null=True,blank=True)
    image = models.ImageField(default="no_image.jpeg" ,upload_to='product_images', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify("product-" + self.name+str(time.time()))
        super(Product, self).save(*args, **kwargs)