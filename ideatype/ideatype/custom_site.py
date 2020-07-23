#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/7/23 15:41
# @Author : zhouzy_a
# @Version：V 0.1
# @File : custom_site.py
# @desc : 自定义后台site


from django.contrib.admin import AdminSite


class CustomSite(AdminSite):
    """自定义后台站点管理之blog管理"""
    site_header = 'my_blog'
    site_title = '个人博客管理后台'
    index_title = '首页'


custom_site = CustomSite(name='cus_admin')

if __name__ == '__main__':
    pass