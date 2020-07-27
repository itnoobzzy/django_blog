from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView

from config.models import SideBar, Link
from .models import Post, Category, Tag
from comment.forms import CommentForm
from comment.models import Comment

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
            'sidebars': self.get_sidebars(),
        })
        context.update(self.get_navs())
        return context

    def get_sidebars(self):
        """得到侧边栏数据"""
        return SideBar.objects.filter(status=SideBar.STATUS_SHOW)


    def get_navs(self):
        """得到导航栏数据"""
        categories = Category.objects.filter(status=Category.STATUS_NORMAL)
        nav_categories = []
        normal_categories = []
        for cate in categories:
            if cate in categories:
                if cate.is_nav:
                    nav_categories.append(cate)
                else:
                    normal_categories.append(cate)

        return {
            'navs': nav_categories,
            'categories': normal_categories
        }



class IndexView(CommentViewMixin, ListView):
    """
    首页类视图函数，设定首页的基础数据集为最新的文章，
    每页显示5个，模板上下文名称模板名称
    """
    queryset = Post.objects.filter(status=Post.STATUS_NORMAL)\
        .select_related('owner')\
        .select_related('category')
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
            'tags': tag
        })
        return context

    def get_queryset(self):
        """重写queryset, 根据标签过滤"""
        queryset = super(TagView, self).get_queryset()
        tag_id = self.kwargs.get('tag_id')
        print("tag_id", tag_id)
        return queryset.filter(tag_id=tag_id)


class PostDetailView(CommentViewMixin, DetailView):
    """文章详情类视图函数"""
    queryset = Post.latest_posts()
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context.update({
            'comment_form': CommentForm,
            'comment_list': Comment.get_by_target(self.request.path)
        })
        return context


class SearchView(IndexView):
    """搜索框类视图函数"""
    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data()
        context.update({
            'keyword': self.request.GET.get('keyword', '')
        })
        return context

    def get_queryset(self):
        queryset = super(SearchView, self).get_queryset()
        keyword = self.request.GET.get('keyword')
        if not keyword:
            return queryset
        return queryset.filter(Q(title_icontains=keyword) | Q(desc_icontains=keyword))


class AuthorView(IndexView):
    """作者信息类视图函数"""
    def get_queryset(self):
        queryset = super(AuthorView, self).get_queryset()
        author_id = self.kwargs.get('owner_id')
        return queryset.filter(owner_id=author_id)


class LinkListView(CommentViewMixin, ListView):
    """友链类视图函数"""
    queryset = Link.objects.filter(status=Link.STATUS_NORMAL)
    template_name = 'config/links.html'
    context_object_name = 'link_list'