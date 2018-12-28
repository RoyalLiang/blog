from django.urls import path, re_path
from .views import *
app_name = 'blog'
urlpatterns = [
    # re_path(r'^article_detail/(?P<kind>.*)/(?P<article_id>.*)/$', ArticleView.as_view(), name='article_detail'),
    path('article/detail/<int:article_id>/', ArticleView.as_view(), name='article_detail'),
    path('share/', ShareView.as_view(), name='share'),
    path('aboutme/', AboutMeView.as_view(), name='aboutme'),
    path('add_comment/', AddCommentView.as_view(), name='add_comment'),
    path('label/', LabelView.as_view(), name='label'),
    path('archive/', TheArchiveView.as_view(), name='archive'),
    # 搜索
    path('search/list/', SearchView.as_view(), name='search_list')
]
