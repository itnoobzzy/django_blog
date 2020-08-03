#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/7/31 11:08
# @Author : zhouzy_a
# @Version：V 0.1
# @File : product.py
# @desc :


from .base import * #NOQA

DEBUG = False

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGING': 'django.db.backends.mysql',
        'NAME': 'typeidea_db',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'CONN_MAX_AGE': 5*60,
        'OPTIONS': {'charset': 'utf8mb4'}
    }
}