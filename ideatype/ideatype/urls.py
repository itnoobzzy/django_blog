"""ideatype URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

# windows在lib/site-packages下创建.pth文件加入custom_site模块路径
from custom_site import custom_site
# linux 用下边的方式
# from ideatype.custom_site import  custom_site

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^blog_admin/', custom_site.urls),
]
