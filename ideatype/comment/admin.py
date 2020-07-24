#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/7/23 15:41
# @Author : zhouzy_a
# @Version：V 0.1
# @File : comment/admin.py
# @desc : 评论admin管理

from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from blog.adminforms import CommentAdminForm
from blog.models import Post
from .models import Comment
# windows 要在lib/site-packages 下建.pth 文件将模块路径放入进去
from custom_site import custom_site
from base_admin import BaseOwnerAdmin
# linux使用下边的方式
# from ideatype.custom_site import comment_site
# from ideatype.base_admin import BaseOwnerAdmin


class TargetOwnerFilter(admin.SimpleListFilter):
    """
    自定义过滤器只显示当前用户的文章
    """
    title = "当前用户所属文章"
    parameter_name = "owner_comment"

    def lookups(self, request, model_admin):
        if request.user.is_superuser:
            return Post.objects.filter().values_list('id', 'title')
        return Post.objects.filter(owner=request.user).values_list('id', 'title')

    def queryset(self, request, queryset):
        target_id = self.value()
        if target_id:
            return queryset.filter(target_id=self.value())
        return queryset


@admin.register(Comment)
@admin.register(Comment, site=custom_site)
class CommentAdmin(BaseOwnerAdmin):
    form = CommentAdminForm
    list_display = ['target', 'nickname', 'content', 'website',
                    'created_time', 'operator']
    list_display_links = ['target', 'website']

    list_filter = [TargetOwnerFilter]

    search_fields = ['target', 'content']

    actions_on_bottom = True
    actions_on_top = True
    save_on_top = True

    exclude = ('nickname',)
    fieldsets = (
        ('基础配置', {
            'description': '基础配置描述',
            'fields': (
                ('website', 'email'),
                'status'
            )
        }),
        (
            '内容', {
                'description': '评论内容',
                'fields': (
                    'content', 'target'
                )
            }
        )
    )

    def operator(self, obj):
        """自定义展示字段"""
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('cus_admin:comment_comment_change', args=(obj.id,))
        )
    operator.short_description = '操作'


