"""ideatype URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import xadmin
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter

from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib.sitemaps import views as sitemap_views
from django.conf import settings

from blog.apis import PostViewSet, CategoryViewSet
from blog.rss import LatestPostFeed
from blog.sitemap import PostSitemap
from .autocomplete import CategoryAutocomplete, TagAutocomplete

from blog.views import (
    IndexView, CategoryView, TagView,
    PostDetailView, AuthorView, SearchView,
    LinkListView
)
from comment.views import CommentView
from config.views import LinkView

router = DefaultRouter()
router.register(r'post', PostViewSet, basename='api-post')
router.register(r'category', CategoryViewSet, basename='api-category')

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^category/(?P<category_id>\d+)/$', CategoryView.as_view(), name='category-list'),
    url(r'^search/$', SearchView.as_view(), name='search'),
    url(r'^tag/(?P<tag_id>\d+)/$', TagView.as_view(), name='tag-list'),
    url(r'^post/(?P<post_id>\d+).html$', PostDetailView.as_view(), name='post-detail'),
    url(r'^links/$', LinkView.as_view(), name='links'),
    url(r'^author/(?P<owner_id>\d+)/$', AuthorView.as_view(), name='author'),
    url(r'^admin/', xadmin.site.urls, name='xadmin'),
    url(r'^links/$', LinkListView.as_view(), name='links'),
    url(r'^comment/$', CommentView.as_view(), name='comment'),

    url(r'^category-autocomplete/$', CategoryAutocomplete.as_view(), name='category-autocomplete'),
    url(r'^tag-autocomplete/$', TagAutocomplete.as_view(), name='tag-autocomplete'),

    url(r'^rss|feed/', LatestPostFeed(), name='rss'),
    url(r'^sitemap\.xml$', sitemap_views.sitemap, {'sitemaps': {'posts': PostSitemap}}),

    url(r'^ckeditor/', include('ckeditor_uploader.urls')),

    url('^api/', include(router.urls, namespace="api")),
    url('^api/docs/', include_docs_urls(title='ideatype apis')),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
