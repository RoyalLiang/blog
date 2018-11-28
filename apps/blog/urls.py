from django.urls import path, re_path
from .views import *
app_name = 'blog'
urlpatterns = [
    re_path(r'^article_detail/(?P<kind>.*)/(?P<article_id>.*)/$', ArticleView.as_view(), name='article_detail'),
    re_path(r'^article_label/(?P<label>.*)/$', ArticleLabel.as_view(), name='article_label'),
    path('share/', ShareView.as_view(), name='share'),
    path('aboutme/', AboutMeView.as_view(), name='aboutme'),

]
