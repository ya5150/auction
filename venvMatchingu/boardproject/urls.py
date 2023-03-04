
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    # ... the rest of your URLconf goes here ...
    path('admin/', admin.site.urls),
    path("",include("boardapp.urls")),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    #urlでsettingのmedia_urlに該当するurlが入力されたら、settingファイルのmedia_rootに指定されたディレクトリからファイルを持ってくる/
    #+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
