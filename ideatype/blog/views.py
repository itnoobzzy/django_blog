from django.shortcuts import render
from django.http import HttpResponse

from config.models import SideBar
from .models import Post, Tag, Category


def post_list(request, category_id=None, tag_id=None):
    """
    默认获取最新文章列表，根据参数分类id和标签id来获取过滤后的文章
    :param request:请求
    :param category_id:分类id
    :param tag_id:标签id
    :return:
    """
    tag = None
    category = None
    if tag_id:
        post_lists, tag = Post.get_by_tag(tag_id)
    elif category_id:
        post_lists, category = Post.get_by_category(category_id)
    else:
        post_lists = Post.latest_posts()

    context = {
        'category': category,
        'tag': tag,
        'post_list': post_lists,
        'sidebars': SideBar.get_all(),
    }
    context.update(Category.get_navs())
    return render(request, 'blog/list.html', context=context)


def post_detail(request, post_id):
    """返回文章详情"""
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        post = None

    context = {
        'post': post,
    }
    context.update(Category.get_navs())
    return render(request, 'blog/detail.html', context=context)