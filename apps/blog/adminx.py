import xadmin
from .models import *


class ArticleAdmin(object):
    list_display = ['title', 'add_time']


class LabelAdmin(object):
    list_display = ['name', 'add_time']


xadmin.site.register(Article, ArticleAdmin)
xadmin.site.register(Label, LabelAdmin)
