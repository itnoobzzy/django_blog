from django.views.generic import ListView

from .models import SideBar, Link


class CommentViewMixin:
    """公共类视图函数处理通用的数据"""
    def get_context_data(self, **kwargs):
        """将所有友链加入模板上下文"""
        context = super(CommentViewMixin, self).get_context_data(**kwargs)
        context.update({
            'links': Link.get_all()
        })
        return context


class LinkView(CommentViewMixin, ListView):
    """友链类视图函数"""
    queryset = Link.get_all()
    # paginate_by = 5
    context_object_name = 'link_list'
    template_name = 'config/blocks/link.html'

