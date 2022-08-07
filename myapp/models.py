from django.db import models

# Create your models here.

from django.db import models
from datetime import datetime

"""
产品中心模型
"""


class Path(models.Model):
    name = models.CharField(max_length=50, verbose_name='名称')
    path = models.CharField(max_length=30, verbose_name='路径')
    type = models.CharField(max_length=30, verbose_name='类型', default='电影')
    status = models.BooleanField(verbose_name='是否启用', default=True)
    create_time = models.DateTimeField(default=datetime.now, verbose_name='创建时间')

    class Meta:
        verbose_name = '资源路径'
        verbose_name_plural = verbose_name
        db_table = 'path'

    def __str__(self):
        return self.path


class Video(models.Model):
    video_name = models.CharField(max_length=50, verbose_name='名称')
    video_path = models.CharField(max_length=30, verbose_name='路径')
    create_time = models.DateTimeField(default=datetime.now, verbose_name='创建时间')

    class Meta:
        verbose_name = '电影'
        verbose_name_plural = verbose_name
        db_table = 'video'

    def __str__(self):
        return self.video_name


class Photo(models.Model):
    image_name = models.CharField(max_length=50, verbose_name='名称')
    image_path = models.FileField('图片地址', default='', upload_to='media/image')
    create_time = models.DateTimeField(default=datetime.now, verbose_name='创建时间')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, verbose_name='电影', blank=True, null=True)

    class Meta:
        verbose_name = '图片'
        verbose_name_plural = verbose_name
        db_table = 'photo'

    def __str__(self):
        return self.image_name