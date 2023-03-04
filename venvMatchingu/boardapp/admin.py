from django.contrib import admin
from .models import *

# 認証画面にモデルを認識させる
admin.site.register(boardmodel)
admin.site.register(Product)
admin.site.register(Product2)
