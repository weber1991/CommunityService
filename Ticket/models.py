from django.db import models
from BUser.models import *

# Create your models


'''
添加窗口的模型：
窗口对账号：一对一关系；（不做一对多，因为要修改用户表，不具有通用性，实则这是种不好的做法）
窗口对业务：一对多；
创建，编辑时间；
窗口名称；
窗口介绍；
备注；
保留项目1；
'''
class BWindow(models.Model):
    name = models.CharField(max_length=255, verbose_name='窗口名称')
    address = models.CharField(max_length=255, verbose_name='窗口地址')
    orderid = models.IntegerField(verbose_name='排序号', default=100)
    show = models.TextField(verbose_name='窗口介绍', blank=True, null=True)
    note = models.TextField(verbose_name='备注', blank=True, null=True)
    hold0 = models.CharField(max_length=255, verbose_name='保留事项')
    addtime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    changetime = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    def __str__(self):
        return self.name
    class Meta:
        verbose_name  = '窗口'
        verbose_name_plural = verbose_name
        ordering = ['orderid']



# 一个窗口，多个业务



class BService(models.Model):
    '''
    业务类型：A,B,C,.....
    业务名称：综合业务、电信业务....
    业务id
    窗口号
    业务状态:开放取号,不开放
    备注
    预留3
    创建时间
    修改时间
    '''
    type = models.CharField(max_length=3, verbose_name='业务类型') # 用来制作票号
    name = models.CharField(max_length=255, verbose_name='业务名称')
    window = models.CharField(max_length=255, verbose_name='窗口名称', null=True, blank=True) # 这里为空，
    state = models.CharField(max_length=125, verbose_name='业务状态')
    note = models.CharField(max_length=255, verbose_name='备注', null=True)
    hold0 = models.CharField(max_length=255, verbose_name='保留1', null=True)
    hold1 = models.CharField(max_length=255, verbose_name='保留2', null=True)
    hold2 = models.CharField(max_length=255, verbose_name='保留3', null=True)
    addtime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    changetime = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name='业务'
        verbose_name_plural = verbose_name


class BWindow2Service(models.Model):
    window = models.ForeignKey(BWindow, verbose_name='窗口号')
    service = models.ForeignKey(BService, verbose_name='业务')
    note = models.TextField(verbose_name='备注', null=True, blank=True)
    addtime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    changetime = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    def __str__(self):
        return '%s的%s'%(self.service, self.window)

    class Meta:
        verbose_name = '窗口与业务关系表'
        verbose_name_plural = verbose_name

'''
人员和窗口进行绑定，然后办理时候自动带入窗口。
'''
class BUser2Window(models.Model):
    user = models.ForeignKey(BUser, verbose_name='办理人')
    window = models.ForeignKey(BWindow,verbose_name='对应窗口')
    note = models.TextField(verbose_name='备注', null=True, blank=True)
    addtime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    changetime = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    def __str__(self):
        return '%s的%s'%(self.user, self.window)

    class Meta:
        verbose_name = '人员窗口关系表'
        verbose_name_plural = verbose_name


class BAssess(models.Model):
    '''办结之后才有评论'''
    # 3满意、2一般、1不满意
    level = models.IntegerField(default=3, verbose_name='评价等级')
    content = models.TextField(verbose_name='评价内容')
    addtime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    changetime = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    def __str__(self):
        return self.level

    class Meta:
        verbose_name = '评价内容'
        verbose_name_plural = verbose_name


class BTicket(models.Model):
    '''
    id
    业务类型
    票号=业务类型+当前数量+1
    票号类型:预约号,现场号---将预约号变为现场号操作
    预约时间(不一定有)-取号时间创建时间-呼号时间-办理时间-办结时间-作废时间
    票号状态:0代表等候,1代表正在办理,2代表已办结,3代表已作废,4代表等待确认预约
    办理人-user
    取号人-wechatuser
    备注:
    预留3
    '''

    no = models.CharField(max_length=6, verbose_name='票号')
    service = models.ForeignKey(BService, verbose_name='业务')
    type = models.BooleanField(verbose_name='票号类型', default=False) # False代表现场号, True代表预约号
    queuetime = models.DateTimeField(verbose_name='预约时间', null=True)
    starttime = models.DateTimeField(verbose_name='取号时间', null=True)
    dotime = models.DateTimeField(verbose_name='办理时间', null=True)
    endtime = models.DateTimeField(verbose_name='办结时间', null=True)
    outtime = models.DateTimeField(verbose_name='作废时间', null=True)
    state = models.IntegerField(verbose_name='票号状态', default=0)
    user = models.ForeignKey(BUser, verbose_name='办理人', null=True)
    window = models.ForeignKey(BWindow, verbose_name='办理窗口', null=True)
    wechatuser = models.ForeignKey(BWechatUser, verbose_name="取号人")
    note = models.TextField(verbose_name='备注',
                            default='备注：每条成功取号信息，除了要显示当前号数以及叫号情况之外，还要提示过号后每个号将延迟两个号再进行业务办理。')
    hold0 = models.CharField(max_length=255, verbose_name='保留', null=True)
    hold1 = models.CharField(max_length=255, verbose_name='保留', null=True)
    hold2 = models.CharField(max_length=255, verbose_name='保留', null=True)
    addtime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    changetime = models.DateTimeField(auto_now=True, verbose_name='修改时间')
    assess = models.OneToOneField(BAssess, verbose_name='票号评价', null=True, blank=True)


    def __str__(self):
        return self.no

    class Meta:
        ordering = ['starttime']
        verbose_name = '票号'
        verbose_name_plural = verbose_name


class Brandonnumber(models.Model):
    number = models.CharField(max_length=255, verbose_name='随机号码')
    state = models.BooleanField(verbose_name='使用状态', default=False)
    addtime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    hold0 = models.CharField(max_length=255, verbose_name='保留', null=True)
    hold1 = models.CharField(max_length=255, verbose_name='保留', null=True)
    hold2 = models.CharField(max_length=255, verbose_name='保留', null=True)
    changetime = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    def __str__(self):
        return self.number

    class Meta:
        verbose_name = '随机码'
        verbose_name_plural = verbose_name


