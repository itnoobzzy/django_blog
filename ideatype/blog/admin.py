from django.contrib.admin.models import LogEntry
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Post, Category, Tag
from .adminforms import PostAdminForm
# windows 要在lib/site-packages 下建.pth 文件将模块路径放入进去
from custom_site import custom_site
from base_admin import BaseOwnerAdmin
# linux使用下边的方式
# from ideatype.custom_site import custom_site
# from ideatype.base_admin import BaseOwnerAdmin


class PostInline(admin.TabularInline):
    """在一个模型编辑内关联另一个模型的编辑，根据主外键关联"""
    fields = ('title', 'desc')  # 显示编辑的字段
    extra = 2   # 额外控制多几个
    model = Post


class CategoryOwnerFilter(admin.SimpleListFilter):
    """
    CategoryOwnerFilter类用于自定义过滤器只展示当前用户分类
    """
    title = "当前用户所属分类"
    parameter_name = "owner_category"

    def lookups(self, request, model_admin):
        """
        返回要展示的内容和查询用的id
        :param request:
        :param model_admin:
        :return:
        """
        if request.user.is_superuser:
            return Category.objects.filter().values_list('id', 'name')
        return Category.objects.filter(owner=request.user).values_list('id', 'name')

    def queryset(self, request, queryset):
        """
        根据url Query 的内容返回列表页数据
        :param request:
        :param queryset:
        :return:
        """
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset


class TagOwnerFilter(admin.SimpleListFilter):
    """
    自定义过滤器只显示当前用户的标签
    """
    title = "当前用户所属标签"
    parameter_name = "owner_tag"

    def lookups(self, request, model_admin):
        if request.user.is_superuser:
            return Tag.objects.filter().values_list('id', 'name')
        return Tag.objects.filter(owner=request.user).values_list('id', 'name')

    def queryset(self, request, queryset):
        target_id = self.value()
        if target_id:
            return queryset.filter(target_id=self.value())
        return queryset


@admin.register(Category)
@admin.register(Category, site=custom_site)
class CategoryAdmin(BaseOwnerAdmin):
    """分类后台管理"""
    inlines = [PostInline]  # 关联文章的模型类
    list_display = ('name', 'status', 'is_nav', 'created_time')
    fields = ('name', 'status', 'is_nav')
    list_filter = [CategoryOwnerFilter]


@admin.register(Tag)
@admin.register(Tag, site=custom_site)
class TagAdmin(BaseOwnerAdmin):
    """标签后台管理"""
    list_display = ('name', "status", 'created_time')
    fields = ('name', 'status')
    list_filter = [TagOwnerFilter]


@admin.register(Post)
@admin.register(Post, site=custom_site)
class PostAdmin(BaseOwnerAdmin):
    """文章后台管理"""
    form = PostAdminForm

    list_display = [
        'title', 'status', 'owner', "category",
        'created_time', 'operator'
    ]

    def show_tag(self, obj):
        return [tag.status for tag in obj.tag.all()]

    list_filter = [CategoryOwnerFilter]
    # filter_horizontal = ('tag',)
    filter_vertical = ('tag',)

    list_display_links = []
    search_fields = ['title', 'category']

    actions_on_top = True
    actions_on_bottom = True

    # 编辑页面
    save_on_top = True

    exclude = ('owner',)

    fieldsets = (
        ('基础配置', {
              'description': '基础配置描述',
              'fields': (
                  ('title', 'category'),
                  'status',
              ),
          }),
        ('内容', {
                'fields': (
                    'desc',
                    'content',
                ),
            }),
        ('额外信息', {
                'classes': ('collapse',),
                'fields': ('tag', ),
            })
    )

    def operator(self, obj):
        """自定义展示字段"""
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('cus_admin:blog_post_change', args=(obj.id,))
        )
    operator.short_description = '操作'


@admin.register(LogEntry, site=custom_site)
class LogEntryAdmin(admin.ModelAdmin):
    """自定义日志记录管理"""
    list_display = ['object_repr', 'object_id', 'action_flag', 'user',
                    'change_message']



