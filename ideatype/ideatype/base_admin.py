#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/7/24 8:38
# @Author : zhouzy_a
# @Version：V 0.1
# @File : base_admin.py
# @desc : 重写save方法与get_queryset方法


from django.contrib import admin


class BaseOwnerAdmin(object):
    """
    1. 用来自动补充文章、分类、标签、侧边栏、友链这些Model 的 owner 字段
    2. 用来针对 queryset 过滤当前用户的数据
    """
    exclude = ('owner', )

    def get_list_queryset(self):
        request = self.request
        qs = super().get_list_queryset()
        return qs.filter(owner=request.user)

    def save_models(self):
        self.new_obj.owner = self.request.user
        return super().save_models()

if __name__ == '__main__':
    pass
