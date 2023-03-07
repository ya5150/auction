from django.test import TestCase
from celery import shared_task

@shared_task
def auction_end_check():
    print("tasukujikkou")
