#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/7/23 15:19
# @Author : zhouzy_a
# @Version：V 0.1
# @File : adminforms.py
# @desc :自定义后台管理Form
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget
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
    content = forms.CharField(widget=forms.HiddenInput(), required=False)
    content_ck = forms.CharField(widget=CKEditorUploadingWidget(), label='正文', required=False)
    content_md = forms.CharField(widget=forms.Textarea(), label='正文', required=False)

    class Meta:
        model = Post
        fields = ('category', 'tag', 'title',
                  'is_md', 'content', 'content_md', 'content_ck',
                  'status')

    def __init__(self, instance=None, initial=None, **kwargs):
        """
        判断文章内容是md格式还是富文本格式
        instance: 当前文章的实例
        initial: Form中各字段初始化的值
        """
        initial = initial or {}
        if instance:
            if instance.is_md:
                initial['content_md'] = instance.content
            else:
                initial['content_ck'] = instance.content

        super(PostAdminForm, self).__init__(instance=instance, initial=initial, **kwargs)

    def clean(self):
        """
        判断是否使用了markdown语法，设置获取对应编辑器的值，并将其赋值给content
        :return:
        """
        is_md = self.cleaned_data.get('is_md')
        if is_md:
            content_field_name = 'content_md'
        else:
            content_field_name = 'content_ck'
        content = self.cleaned_data.get(content_field_name)
        if not content:
            self.add_error(content_field_name, '必须填！')
            return
        self.cleaned_data['content'] = content
        return super().clean()

    class Media:
        js = ('js/post_editor.js',)


class CommentAdminForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea, label='内容', required=True)


