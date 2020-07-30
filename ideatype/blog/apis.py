#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/7/30 13:27
# @Author : zhouzy_a
# @Version：V 0.1
# @File : apis.py
# @desc :
from rest_framework import generics, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from blog.models import Post, Category
from blog.serializers import (
    PostSerializer, PostDetailSerializer,
    CategorySerializer,
    CategoryDetailSerializer)


class PostViewSet(viewsets.ModelViewSet):
    """序列化文章模型类视图函数"""
    serializer_class = PostSerializer
    queryset = Post.objects.filter(status=Post.STATUS_NORMAL)

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = PostDetailSerializer
        return super(PostViewSet, self).retrieve(request, *args, **kwargs)

    def filter_queryset(self, queryset):
        category_id = self.request.query_params.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """序列化分类模型类视图函数"""
    serializer_class = CategorySerializer
    queryset = Category.objects.filter(status=Category.STATUS_NORMAL)

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = CategoryDetailSerializer
        return super(CategoryViewSet, self).retrieve(request, *args, *kwargs)