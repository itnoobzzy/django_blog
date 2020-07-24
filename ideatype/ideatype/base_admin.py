#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/7/24 8:38
# @Author : zhouzy_a
# @Version：V 0.1
# @File : base_admin.py
# @desc : 重写save方法与get_queryset方法


from django.contrib import admin


class BaseOwnerAdmin(admin.ModelAdmin):
    """
    1. 用来自动补充文章、分类、标签、侧边栏、友链这些Model 的 owner 字段
    2. 用来针对 queryset 过滤当前用户的数据
    """
    exclude = ('owner', )

    def get_queryset(self, request):
        qs = super(BaseOwnerAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(BaseOwnerAdmin, self).save_model(request, obj, form, change)

if __name__ == '__main__':
    pass