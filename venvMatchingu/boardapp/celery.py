import os
from celery import Celery
from django.conf import settings

# プロジェクトのDjangoの設定ファイルを環境変数DJANGO_SETTINGS_MODULEから読み込む
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boardproject.settings')

app = Celery('boardapp')

# Djangoの設定ファイルの中でCELERY_から始まる変数をCeleryアプリの設定に追加する
app.config_from_object('django.conf:settings', namespace='CELERY')

# アプリを自動検出する
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS + ['boardapp'])
import os
from celery import Celery
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yourproject.settings')

app = Celery('yourproject', broker=settings.CELERY_BROKER_URL)

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
from celery import Celery

app = Celery('proj')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# CELERY_IMPORTS の設定
CELERY_IMPORTS = (
    "boardapp.task",
)
