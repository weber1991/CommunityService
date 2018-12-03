from django.db import models

# Create your models here.

class WechatAccessToken(models.Model):
    access_token = models.CharField(max_length=512, verbose_name='微信接口凭证')
    addTime = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    def __str__(self):
        return self.access_token

    class Meta:
        app_label="wechatMessage"
        verbose_name_plural="微信凭证管理"
        verbose_name="微信凭证管理"