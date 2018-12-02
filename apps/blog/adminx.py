import xadmin
from .models import *
from mdeditor.widgets import MDEditorWidget


class ArticleAdmin(object):
    list_display = ['title', 'add_time']
    formfield_overrides = {
        models.TextField: {'widget': MDEditorWidget}
    }


class LabelAdmin(object):
    list_display = ['name', 'add_time']


xadmin.site.register(Article, ArticleAdmin)
xadmin.site.register(Label, LabelAdmin)
