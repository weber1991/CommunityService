from django.db import models
from BUser.models import BWechatUser
# Create your models here.


'''
1、留言模型：
a、群众部分：留言人，留言时间，联系方式，留言题目，留言内容，上传附件（动态）
b、书记部分：回复内容（附带图片），回复人，回复时间
c、留言状态（公开，私密，隐藏），留言进度（待回复-待发送-办结）
2、模板信息提示回复，跳转到信箱详细内容
3、查看历史留言功能（前台JS实现排序，分类，分页等。）
扩展：
1、设置用户，收到留言后有微信模板信息提示
'''

class Message(models.Model):
    sendname = models.CharField(max_length=255, verbose_name='留言人')
    sendtime = models.DateTimeField(auto_now_add=True, verbose_name='留言时间')
    sendphone = models.CharField(max_length=22, verbose_name='联系方式')
    sendtitle = models.CharField(max_length=255, verbose_name='留言标题')
    sendcontent = models.TextField(verbose_name='留言内容')
    # img
    # 先用文本编辑器来实现多图上传

    backname = models.CharField(max_length=255, verbose_name='回复人', null=True, blank=True)
    backtime = models.DateTimeField(auto_now=True, verbose_name='回复时间')
    backcontent = models.TextField(verbose_name='回复内容', null=True, blank=True)

    state = models.CharField(max_length=11, verbose_name='留言状态', default='私密')
    process = models.CharField(max_length=11, verbose_name='留言进度', default='待回复')
    wechat = models.ForeignKey(BWechatUser, verbose_name='微信用户', null=True, blank=True)
    file0 = models.FileField(verbose_name='文件', upload_to='media/message', default='', null=True, blank=True)
    file1 = models.FileField(verbose_name='文件', upload_to='media/message', default='', null=True, blank=True)
    file2 = models.FileField(verbose_name='文件', upload_to='media/message',  default='', null=True, blank=True)
    file3 = models.FileField(verbose_name='文件', upload_to='media/message', default='', null=True, blank=True)

    def __str__(self):
        return self.sendtitle

    class Meta:
        verbose_name = '留言管理'
        verbose_name_plural = '留言管理'
