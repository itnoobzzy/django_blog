#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/7/28 14:21
# @Author : zhouzy_a
# @Version：V 0.1
# @File : autocomplete.py
# @desc :配置需要自动补全的接口


from dal import autocomplete

from blog.models import Category, Tag


class CategoryAutocomplete(autocomplete.Select2QuerySetView):
    """自动补全分类查询内容"""
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Category.objects.none()

        qs = Category.objects.filter(owner=self.request.user)

        if self.q:
            qs = qs.filter(name__contains=self.q)
        return qs


class TagAutocomplete(autocomplete.Select2QuerySetView):
    """自动补全标签查询"""
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Tag.objects.none()

        qs = Tag.objects.all()

        if self.q:
            qs = qs.filter(name__contains=self.q)
        return qs

