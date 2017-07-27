from __future__ import unicode_literals

from django.db import models


# Create your models here.

class Project(models.Model):
    """
    爬虫项目
    """
    name = models.CharField('项目名称', max_length=50)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    status = models.IntegerField('状态', default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '生活圈'
        verbose_name_plural = '生活圈列表'


class EntryPoint(models.Model):
    """
    爬虫入口网页
    """
    project = models.ForeignKey(Project, null=True, verbose_name="项目")
    name = models.CharField(max_length=50, verbose_name='名称')
    url = models.CharField(max_length=255, verbose_name='入口页面')
    url_pattern = models.CharField(max_length=255, verbose_name='抓取网页的URL正则表达式')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    default_freq = models.IntegerField('默认的频率', help_text='单位秒', default=600)
    title_selector = models.CharField(max_length=255, verbose_name='标题选择器', null=True, blank=True)
    body_selector = models.CharField(max_length=255, verbose_name='正文选择器', null=True, blank=True)
    status = models.IntegerField(default=0, help_text='0为正常', verbose_name="状态")
    last_exec_time = models.DateTimeField('最后执行时间', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '入口页'
        verbose_name_plural = ' 入口页列表'


class Item(models.Model):
    """
    爬下来的网页列表
    """
    entry = models.ForeignKey(EntryPoint)
    url_md5 = models.CharField(max_length=32, verbose_name='网页ID', unique=True)
    url = models.CharField(max_length=255, verbose_name='URL')
    content = models.TextField(blank=True, null=True, verbose_name='网页内容')
    title = models.CharField('文章标题', max_length=255, blank=True)
    created_at = models.DateTimeField('抓取时间', auto_now_add=True)
