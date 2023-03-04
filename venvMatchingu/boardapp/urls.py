from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    # このパスにアクセスすると、views.pyのsignupfunc関数が呼び出されます
    path('signup/', views.signupfunc, name='signup'),
    path('login/', views.loginfunc, name='login'),
    path("list/", views.listfunc, name="list"),
    path("logout/", views.logoutfunc, name="logout"),
    path("detail/<int:pk>", views.detailfunc, name="detail"),
    path("good/<int:pk>", views.goodfunc, name="good"),
    path("read/<int:pk>", views.readfunc, name="read"),
    path("create/",views.boardcreate.as_view(), name="create"),
    path('product/<int:user_id>', views.user_products, name='user_products'),
    path('product/<slug:slug>', views.product_detail, name='product_detail'),
    path('productcreate/', views.productcreate, name='productcreate'),
    path('productlist/', views.Productlist.as_view(), name='Productlist'),

]

