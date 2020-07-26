from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, ListView

from config.models import SideBar
from .models import Post, Category, Tag

'''
未使用类视图函数的写法
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
'''


class CommentViewMixin:
    """
    公共类视图函数处理通用的数据: 导航栏列表和侧边栏列表
    """
    def get_context_data(self, **kwargs):
        """将导航栏列表和侧边栏列表的数据加入模板上下文"""
        context = super(CommentViewMixin, self).get_context_data(**kwargs)
        context.update({
            'sidebars': SideBar.get_all()
        })
        context.update(Category.get_navs())
        return context


class IndexView(CommentViewMixin, ListView):
    """
    首页类视图函数，设定首页的基础数据集为最新的文章，
    每页显示5个，模板上下文名称模板名称
    """
    queryset = Post.latest_posts()
    paginate_by = 5
    context_object_name = 'post_list'
    template_name = 'blog/list.html'


class CategoryView(IndexView):
    """
    分类列表页类视图函数
    """
    def get_context_data(self, **kwargs):
        """将分类加入上下文"""
        context = super(CategoryView, self).get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, pk=category_id)
        context.update({
            'category': category,
        })
        return context

    def get_queryset(self):
        """重写queryset，根据分类过滤"""
        queryset = super(CategoryView, self).get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id)


class TagView(IndexView):
    """标签列表类视图函数"""
    def get_context_data(self, **kwargs):
        """标签加入上下文"""
        context = super(TagView, self).get_context_data(**kwargs)
        tag_id = self.kwargs.get('tag_id')
        tag = get_object_or_404(Tag, pk=tag_id)
        context.update({
            'tag': tag
        })
        return context

    def get_queryset(self):
        """重写queryset, 根据标签过滤"""
        queryset = super(TagView, self).get_queryset()
        tag_id = self.kwargs.get('tag_id')
        return queryset.filter(tag_id=tag_id)


class PostDetailView(CommentViewMixin, DetailView):
    """文章详情类视图函数"""
    queryset = Post.latest_posts()
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'


