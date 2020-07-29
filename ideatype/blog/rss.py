#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/7/29 13:14
# @Author : zhouzy_a
# @Version：V 0.1
# @File : rss.py
# @desc :订阅接口
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Rss201rev2Feed

from blog.models import Post


class ExtendedRSSFeed(Rss201rev2Feed):
    def add_item_elements(self, handler, item):
        super(ExtendedRSSFeed, self).add_item_elements(handler, item)
        handler.addQuickElement('content:html', item['content_html'])


class LatestPostFeed(Feed):
    """RSS阅读器"""
    feed_type = Rss201rev2Feed
    title = "Typeidea Blog System"
    link = "/rss/"
    description = "typeidea is a blog system power by django"

    def iterms(self):
        return Post.objects.filter(status=Post.STATUS_NORMAL)[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.title

    def item_link(self, item):
        return reversed('post-detail', args=[item.pk])

    def item_extra_kwargs(self, item):
        return {'content_html': self.item_content_html(item)}

    def item_content_item(self, item):
        return item.content_html



