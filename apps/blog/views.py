from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from .models import *
from pure_pagination import PageNotAnInteger, Paginator
from .forms import CommentForm, ShareForm
from .send_mail import send_email


# Create your views here.


class IndexView(View):
    def get(self, request):
        links = 'index'
        all_article = Article.objects.all().order_by('-click_nums')
        articles = Article.objects.all().order_by('-add_time')[:1]
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # per_page:每页显示的条目个数
        p = Paginator(all_article, request=request, per_page=6)

        all_articles = p.page(page)
        return render(request, 'index.html', {
            'all_articles': all_articles,
            'articles': articles,
            'links': links,
        })


class ArticleView(View):
    def get(self, request, article_id, kind):
        links = 'read'
        article = Article.objects.get(pk=article_id)
        all_comments = article.comment_set.all()
        comment_nums = all_comments.count()
        article.click_nums += 1
        article.save()
        return render(request, 'articledetail.html', {
            'article': article,
            'all_comments': all_comments,
            'comment_nums': comment_nums,
            'links': links,
            'kind': kind,
        })


# 发表评论
class AddCommentView(View):
    def post(self, request):
        print(True)
        article_id = request.POST.get('article_id', 0)
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        comment = request.POST.get('comments', '')

        if int(article_id) > 0 and comment and name and email:
            print('Hello World')
            article_comment = Comment()
            article = Article.objects.get(pk=int(article_id))
            article_comment.comment_article = article
            article_comment.name = name
            article_comment.email = email
            article_comment.message = comment
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
            return render(request, 'index.html', {})


class ArticleLabel(View):
    def get(self, request, label):
        # python视图
        if label == 'python':
            links = 'python'
            all_article = Article.objects.filter(article_label_id=1)
            return render(request, 'python-list.html', {
                'all_article': all_article,
                'links': links,
            })
        # 前端视图
        elif label == 'front':
            links = 'front'
            all_article = Article.objects.filter(article_label_id=2)
            return render(request, 'qianduan-list.html', {
                'all_article': all_article,
                'links': links,

            })
        # 数据库视图
        elif label == 'database':
            links = 'database'
            all_article = Article.objects.filter(article_label_id=3)
            return render(request, 'database-list.html', {
                'all_article': all_article,
                'links': links,

            })
        # 杂记视图
        elif label == 'zaji':
            links = 'zaji'
            all_article = Article.objects.filter(article_label_id=4)
            return render(request, 'zaji-list.html', {
                'all_article': all_article,
                'links': links,

            })


class AboutMeView(View):
    def get(self, request):
        links = 'aboutme'
        return render(request, 'aboutme.html', {
            'links': links,
        })
