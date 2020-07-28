#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/7/23 15:19
# @Author : zhouzy_a
# @Version：V 0.1
# @File : adminforms.py
# @desc :自定义后台管理Form
from dal import autocomplete
from django import forms

from blog.models import Category, Tag, Post


class PostAdminForm(forms.ModelForm):
    """自定义文章form"""
    desc = forms.CharField(widget=forms.Textarea, label='摘要', required=False)
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=autocomplete.ModelSelect2(url='category-autocomplete'),
        label='分类'
    )
    tag = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=autocomplete.ModelSelect2Multiple(url='tag-autocomplete'),
        label='标签'
    )

    class Meta:
        model = Post
        fields = ('category', 'tag', 'title', 'content', 'status')


class CommentAdminForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea, label='内容', required=True)


if __name__ == '__main__':
    pass