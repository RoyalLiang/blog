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
        article = Article.objects.get(pk=int(article_id))
        comments = Comment.objects.filter(comment_article_id=article_id)
        comment_nums = comments.count()
        article.click_nums += 1
        article.save()
        return render(request, 'articledetail.html', {
            'article': article,
            'comments': comments,
            'comment_nums': comment_nums,
            'links': links,
            'kind': kind,
        })

    def post(self, request, article_id, kind):
        comment_form = CommentForm(request.POST)
        article = Article.objects.get(pk=article_id)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            # 设置外键为当前文章
            new_comment.comment_article = article
            # 将评论数据对象写入数据库
            new_comment.save()
            comments = Comment.objects.filter(comment_article_id=article_id)
            comment_nums = comments.count()
            return render(request, 'articledetail.html', {
                'comments': comments,
                'article': article,
                'comment_nums': comment_nums,
                'kind': kind,
            })
        else:
            comments = Comment.objects.filter(comment_article_id=article_id)
            comment_nums = comments.count()
            return render(request, 'articledetail.html', {
                'msg': comment_form,
                'article': article,
                'comments': comments,
                'comment_nums': comment_nums,
                'kind': kind,

            })


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
