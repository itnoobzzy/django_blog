#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/7/27 14:40
# @Author : zhouzy_a
# @Version：V 0.1
# @File : forms.py
# @desc :评论form验证
import mistune

from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    """评论的form"""
    nickname = forms.CharField(
        label='昵称',
        max_length=50,
        widget=forms.widgets.Input(
            attrs={'class': 'form-control', 'style': 'width: 60%'}
        )
    )
    email = forms.CharField(
        label='Email',
        max_length=50,
        widget=forms.widgets.EmailInput(
            attrs={'class': 'form-control', 'style': 'width: 60%'}
        )
    )
    website = forms.CharField(
        label='网站',
        max_length=100,
        widget=forms.widgets.URLInput(
            attrs={'class': 'form-control', 'style': 'width: 60%'}
        )
    )
    content = forms.CharField(
        label='内容',
        max_length=500,
        widget=forms.widgets.Textarea(
            attrs={'rows': 6, 'cols': 60, 'class': 'form-control'}
        )
    )

    def clean_content(self):
        """处理对应字段数据"""
        content = self.cleaned_data.get('content')
        content = mistune.markdown(content)
        return content

    class Meta:
        model = Comment
        fields = ['nickname', 'email', 'website', 'content']






if __name__ == '__main__':
    pass