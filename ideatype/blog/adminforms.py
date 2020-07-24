#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/7/23 15:19
# @Author : zhouzy_a
# @Version：V 0.1
# @File : adminforms.py
# @desc :自定义后台管理Form

from django import forms


class PostAdminForm(forms.ModelForm):
    desc = forms.CharField(widget=forms.Textarea, label='摘要', required=False)


class CommentAdminForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea, label='内容', required=True)


if __name__ == '__main__':
    pass