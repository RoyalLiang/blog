from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from mdeditor.fields import MDTextField
import re
# Create your models here.


# 标签
class Label(models.Model):
    name = models.CharField(verbose_name='标签名', max_length=16)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "标签"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Article(models.Model):
    article_author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者', null=True, blank=True)
    article_label = models.ManyToManyField(Label, verbose_name='文章类别')
    title = models.CharField(max_length=32, verbose_name='标题')
    excerpt = models.CharField(max_length=300, blank=True, verbose_name='摘要', null=True)  # 摘要
    image = models.ImageField(upload_to='article/%Y/%m', verbose_name='文章配图', null=True, blank=True)
    content = MDTextField(verbose_name='内容')
    click_nums = models.PositiveIntegerField(default=0, verbose_name='阅读量')
    add_time = models.DateTimeField(default=datetime.now, verbose_name="发表时间")

    class Meta:
        verbose_name = "文章"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # 从 body 摘取前 200 个字符赋给到 excerpt
        content = re.sub(' ', '', self.content)
        content = re.sub('#', '', content)
        self.excerpt = content[:200]

        # 调用父类的 save 方法将数据保存到数据库中
        super(Article, self).save(*args, **kwargs)

    def increase_click_nums(self):
        self.click_nums += 1
        self.save(update_fields=['click_nums'])


class Comment(models.Model):
    comment_article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='评论文章')
    name = models.CharField(max_length=24, verbose_name='昵称')
    email = models.EmailField(verbose_name='邮箱')
    message = models.TextField(verbose_name='内容')
    add_time = models.DateTimeField(default=datetime.now, verbose_name="发布时间")

    class Meta:
        verbose_name = "评论"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name





