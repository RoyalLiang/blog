from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from .models import *
from pure_pagination import PageNotAnInteger, Paginator
from .forms import CommentForm, ShareForm
from .send_mail import send_email
import markdown
from django.db.models import Q
from django.contrib.auth.models import User


# Create your views here.


class IndexView(View):
    def get(self, request):
        links = 'index'
        all_article = Article.objects.all().order_by('-add_time')
        latest_article = Article.objects.all().order_by('-add_time')[:3]
        latest_comment = Comment.objects.all().order_by('-add_time')[:5]
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # per_page:每页显示的条目个数
        p = Paginator(all_article, request=request, per_page=9)

        all_articles = p.page(page)
        return render(request, 'index.html', {
            'all_articles': all_articles,
            'links': links,
            'latest_article': latest_article,
            'latest_comment': latest_comment,
        })


class ArticleView(View):
    def get(self, request, article_id):
        article = Article.objects.get(pk=article_id)
        latest_article = Article.objects.all().order_by('-add_time')[:3]
        latest_comment = Comment.objects.all().order_by('-add_time')[:5]
        article.content = markdown.markdown(article.content, extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ], safe_mode=True, enable_attributes=False)
        all_comments = article.comment_set.all()
        comment_nums = all_comments.count()
        article.increase_click_nums()
        return render(request, 'article-detail.html', {
            'article': article,
            'all_comments': all_comments,
            'comment_nums': comment_nums,
            'latest_article': latest_article,
            'latest_comment': latest_comment,
        })


# 发表评论
class AddCommentView(View):
    def post(self, request):
        article_id = request.POST.get('article_id', 0)
        comment_form = CommentForm(request.POST)
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        message = request.POST.get('message', '')

        if int(article_id) > 0 and comment_form.is_valid():
            article_comment = Comment()
            article = Article.objects.get(pk=int(article_id))
            article_comment.comment_article = article
            article_comment.name = name
            article_comment.email = email
            article_comment.message = message
            article_comment.save()
            return HttpResponse('{"status": "success", "msg": "评论成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status": "fail", "msg": "评论失败"}', content_type='application/json')


class ShareView(View):
    def get(self, request):
        return render(request, 'share.html', {})

    def post(self, request):
        share_form = ShareForm(request.POST)
        if share_form.is_valid():
            name = request.POST.get('name', '')
            email = request.POST.get('email', '')
            message = request.POST.get('message', '')
            send_email(email, name, message)
            return render(request, 'send-success.html', {})
        else:
            return render(request, 'share.html', {
                'share_form': share_form,
            })


class LabelView(View):
    def get(self, request):
        all_label = Label.objects.all()
        all_label_article = {}.fromkeys([label for label in all_label], [])
        for label in all_label:
            label_article = Article.objects.filter(article_label=label).order_by('-add_time')
            all_label_article[label] = label_article
        latest_article = Article.objects.all().order_by('-add_time')[:3]
        latest_comment = Comment.objects.all().order_by('-add_time')[:5]
        return render(request, 'label-list.html', {
            'latest_article': latest_article,
            'latest_comment': latest_comment,
            'all_label_article': all_label_article,
        })


class AboutMeView(View):
    def get(self, request):
        latest_article = Article.objects.all().order_by('-add_time')[:3]
        latest_comment = Comment.objects.all().order_by('-add_time')[:5]
        user = User.objects.get(pk=1)
        return render(request, 'aboutme.html', {
            'latest_article': latest_article,
            'latest_comment': latest_comment,
            'user': user,
        })


# 归档视图
class TheArchiveView(View):
    def get(self, request):
        all_article = Article.objects.all().order_by('-add_time')
        latest_article = Article.objects.all().order_by('-add_time')[:3]
        latest_comment = Comment.objects.all().order_by('-add_time')[:5]
        return render(request, 'archives.html', {
            'all_article': all_article,
            'latest_article': latest_article,
            'latest_comment': latest_comment,
        })


class SearchView(View):
    def get(self, request):
        search_keywords = request.GET.get('search', '')
        latest_article = Article.objects.all().order_by('-add_time')[:3]
        latest_comment = Comment.objects.all().order_by('-add_time')[:5]
        all_search = Article.objects.all()
        if search_keywords is not None:
            all_search = all_search.filter(Q(title__icontains=search_keywords))
        return render(request, 'search-list.html', {
            'all_search': all_search,
            'latest_article': latest_article,
            'latest_comment': latest_comment,
        })
