from django import forms
from .models import *


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'message']
        # widgets = {
        #     'message': forms.Textarea(
        #         attrs={
        #             'style': 'height: 200px;width: 100px'
        #         }
        #     ),
        # }


class ShareForm(forms.Form):
    name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    message = forms.Textarea()


class MDEditorModleForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = '__all__'
