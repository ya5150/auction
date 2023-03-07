# tasks.py
from celery import shared_task
from django.utils import timezone
from .models import Product

@shared_task
def auction_end_check():
    print("タスク実行中")
    products = Product.objects.filter(sold=False, end_time__lte=timezone.now())
    for product in products:
        product.sold = True
        product.save()

