
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Post, Category, Tag
from .adminforms import PostAdminForm
from custom_site import custom_site
# Register your models here.

class PostInline(admin.TabularInline):
    """在一个模型编辑内关联另一个模型的编辑，根据主外键关联"""
    fields = ('title', 'desc')  # 显示编辑的字段
    extra = 2   # 额外控制多几个
    model = Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """分类后台管理"""
    inlines = [PostInline]  # 关联文章的模型类
    list_display = ('name', 'status', 'is_nav', 'created_time')
    fields = ('name', 'status', 'is_nav', 'owner')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(CategoryAdmin, self).save_model(request, obj, form, change)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """标签后台管理"""
    list_display = ('name', "status", 'created_time')
    fields = ('name', 'status')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(TagAdmin, self).save_model(request, obj, form, change)


class CategoryOwnerFilter(admin.SimpleListFilter):
    """
    CategoryOwnerFilter类用于自定义过滤器只展示当前用户分类
    """
    title = "分类过滤器"
    parameter_name = "owner_category"
    def lookups(self, request, model_admin):
        """
        返回要展示的内容和查询用的id
        :param request:
        :param model_admin:
        :return:
        """
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


@admin.register(Post, site=custom_site)
class PostAdmin(admin.ModelAdmin):
    """文章后台管理"""
    form = PostAdminForm

    list_display = [
        'title', 'status', "show_tag", "category",
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

    def save_model(self, request, obj, form, change):
        """保存时设置作者为当前用户"""
        obj.owner = request.user
        return super(PostAdmin, self).save_model(request, obj, form, change)

    def get_queryset(self, request):
        """自定义过滤使查询到的作者为登录用户"""
        qs = super(PostAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)


