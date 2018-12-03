from django.db import models
import django.utils.timezone as timezone

# Create your models here.



class BUser(models.Model):
    name = models.CharField(max_length=255, verbose_name='用户名',null=True,blank=True,default='')
    idcard = models.CharField(max_length=20,verbose_name='身份证', null=True,blank=True,default='')
    phone = models.CharField(max_length=11, verbose_name='手机号码',null=True,blank=True, default='')
    email = models.EmailField(verbose_name='电子邮箱', null=True,blank=True, default='')
    username = models.CharField(max_length=255, verbose_name='用户账号',null=True,blank=True, default='')
    password = models.CharField(max_length=255, verbose_name='用户密码',null=True,blank=True, default='')
    logo = models.ImageField(upload_to='BUser/logo', verbose_name='用户头像', default='BUser/logo/人.png')
    hold0 = models.CharField(max_length=255, verbose_name='预留字段0',null=True,blank=True,default='')
    hold1 = models.CharField(max_length=255, verbose_name='预留字段1', null=True,blank=True, default='')
    hold2 = models.CharField(max_length=255, verbose_name='预留字段2', null=True,blank=True, default='')
    hold3 = models.CharField(max_length=255, verbose_name='预留字段3', null=True,blank=True, default='')
    addtime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    changetime = models.DateTimeField(verbose_name='修改时间', auto_now=True)
    # 权限分布，梗合理的做法是用一对一关系
    # 0代表无权限，1代表办事员，2代表管理员

    blog = models.IntegerField(verbose_name='博客权限',default=0)
    webword = models.IntegerField(verbose_name='网上办事权限',default=0)
    ticket = models.IntegerField(verbose_name='叫号权限',default=0)
    message = models.IntegerField(verbose_name='留言权限',default=0)
    person = models.IntegerField(verbose_name='人员权限',default=0)
    issuper = models.IntegerField(verbose_name='超级管理员标志',default=0)
    def __str__(self):
        return self.username

    class Meta:
        verbose_name = '用户记录'
        verbose_name_plural = '用户记录'


class BWechatUser(models.Model):
    openid = models.CharField(max_length=255, verbose_name='用户识别号')
    name = models.CharField(max_length=255, verbose_name='用户名', null=True, blank=True, default='')
    idcard = models.CharField(max_length=20, verbose_name='身份证', null=True, blank=True, default='')
    phone = models.CharField(max_length=11, verbose_name='手机号码', null=True, blank=True, default='')
    email = models.EmailField(verbose_name='电子邮箱', null=True, blank=True, default='')
    logo = models.ImageField(upload_to='BUser/logo', verbose_name='用户头像', default='BUser/logo/人.png')
    hold0 = models.CharField(max_length=255, verbose_name='预留字段0', null=True, blank=True, default='')
    hold1 = models.CharField(max_length=255, verbose_name='预留字段1', null=True, blank=True, default='')
    hold2 = models.CharField(max_length=255, verbose_name='预留字段2', null=True, blank=True, default='')
    hold3 = models.CharField(max_length=255, verbose_name='预留字段3', null=True, blank=True, default='')
    addtime = models.DateTimeField(verbose_name='创建时间', auto_now_add=True,)
    changetime = models.DateTimeField(verbose_name='修改时间', auto_now=True,)

    
    def __str__(self):
        if self.name is None:
            return self.openid
        else:
            return self.name

    class Meta:
        verbose_name = '微信用户'
        verbose_name_plural = '微信用户'
