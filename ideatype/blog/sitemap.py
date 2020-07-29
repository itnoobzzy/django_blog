#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/7/29 13:30
# @Author : zhouzy_a
# @Version：V 0.1
# @File : sitemap.py
# @desc :站点地图
from django.contrib.sitemaps import Sitemap

from blog.models import Post


class PostSitemap(Sitemap):
    """站点地图"""
    changefreq = "always"
    priority = 1.0
    protocol = 'https'

    def items(self):
        """返回所有的NOMAL文章"""
        return Post.objects.filter(status=Post.STATUS_NORMAL)

    def lastmod(self, obj):
        """返回每篇文章的更新时间"""
        return obj.created_item

    def location(self, obj):
        """返回每篇文章的URL"""
        return reversed('post-detail', args=[obj.pk])
