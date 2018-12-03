from django.db import models


# Create your models here.
class CommunityBase(models.Model):
    title = models.CharField(max_length=512, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    author = models.CharField(max_length=255, verbose_name='作者')
    keep1 = models.CharField(max_length=512, verbose_name='保留1', default='', null=True, blank=True)
    keep2 = models.CharField(max_length=512, verbose_name='保留2', default='', null=True, blank=True)
    keep3 = models.CharField(max_length=512, verbose_name='保留3', default='', null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '基础信息表'
        verbose_name_plural = '基础信息表'