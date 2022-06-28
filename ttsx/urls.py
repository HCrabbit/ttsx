"""ttsx URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from goods import views as views_goods
from cart import views as views_cart

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views_goods.index), #主页
    path('detail/', views_goods.detail), #详情页
    path('cart/add_cart/', views_cart.add_cart), #添加购物车页面
    path('goods/', views_goods.goods), # 商品分类页面
    path('cart/show_cart/', views_cart.show_cart), # 购物车页面
    path('cart/remove_cart/', views_cart.remove_cart), # 购物车删除页面
    path('cart/place_order/', views_cart.place_order), # 提交订单的页面显示
    path('cart/submit_order/', views_cart.submit_order), #提交订单功能
    path('cart/submit_success/', views_cart.submit_success), # 提交成功页面
]
