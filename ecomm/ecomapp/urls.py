"""
URL configuration for ecomm project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from .import views as v
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
 
    path('', v.home, name='home'),
    path('about',v.about),
    path('contact',v.contact),
    path('pdetails/<rid>',v.product_details),
    path('register',v.register),
    path('login',v.user_login),
    path('logout',v.user_logout),   
    path('catfilter/<rid>',v.prod_filter),
    path('sort/<rid>',v.sort),
    path('range',v.range),
    path('search',v.prod_search),
    path('addtocart/<pid>',v.addtocart),
    path('viewcart',v.viewcart),
    path('updateqty/<x>/<cid>',v.updateqty),
    path('removecart/<rid>',v.removecart),
    path('placeorder',v.placeorder),
    path('makepayment',v.makepayment),
    path('order',v.order),
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
