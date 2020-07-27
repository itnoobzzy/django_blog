#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/7/27 16:23
# @Author : zhouzy_a
# @Version：V 0.1
# @File : comment_block.py
# @desc :自定义评论模块标签

from django import template
from comment.forms import CommentForm
from comment.models import Comment

register = template.Library()


@register.inclusion_tag('comment/block.html')
def comment_block(target):
    """评论模块"""
    return {
        'target': target,
        'comment_form': CommentForm(),
        'comment_list': Comment.get_by_target(target)
    }


if __name__ == '__main__':
    pass