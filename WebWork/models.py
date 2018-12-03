from django.db import models
from BUser.models import *

# Create your models here.

# 社区简介：
# 联系我们：
# 留言信箱：
# 微信用户：需要记录openid来发送模板信息
# 动态资讯：

# 网上办事系统
'''
1、登记事项信息，还有标签
2、群众点击办理事项-页面提交资料（上传附件）-后台查看-接受or拒绝订单-发送模板消息
3、
'''

'''
前台实现事项搜索：
1、用js直接实现
2、用ajax类似加载更多数据那样实现
3、直接用jmb的来搜索
'''

class ShiXiangType(models.Model):
    name = models.CharField(max_length=50, verbose_name='事项类型')
    addtime = models.TimeField(verbose_name='创建时间',auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '事项类型'
        verbose_name = '事项类型'
        ordering = ['id']


class ShiXiang(models.Model):
    import datetime
    bh = models.BigAutoField(verbose_name='事项编号', primary_key=True)
    name = models.CharField(max_length=511, verbose_name='事项名称')
    cjsj = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    sxzt = models.CharField(max_length=50, verbose_name='事项状态', default='草稿')
    type = models.ForeignKey(ShiXiangType, verbose_name='事项类型')
    file0 = models.FileField(upload_to='WebWork/', verbose_name='附件', default='',null=True, blank=True)
    file1 = models.FileField(upload_to='WebWork/', verbose_name='附件', default='',null=True, blank=True)
    file2 = models.FileField(upload_to='WebWork/', verbose_name='附件', default='',null=True, blank=True)
    file3 = models.FileField(upload_to='WebWork/', verbose_name='附件', default='',null=True, blank=True)
    file4 = models.FileField(upload_to='WebWork/', verbose_name='附件', default='',null=True, blank=True)
    file5 = models.FileField(upload_to='WebWork/', verbose_name='附件', default='',null=True, blank=True)
    file6 = models.FileField(upload_to='WebWork/', verbose_name='附件', default='',null=True, blank=True)
    file7 = models.FileField(upload_to='WebWork/', verbose_name='附件', default='',null=True, blank=True)
    file8 = models.FileField(upload_to='WebWork/', verbose_name='附件', default='',null=True, blank=True)
    file9 = models.FileField(upload_to='WebWork/', verbose_name='附件', default='',null=True, blank=True)
    note0 = models.CharField(max_length=255, verbose_name='附件说明', null=True, blank=True)
    note1 = models.CharField(max_length=255, verbose_name='附件说明', null=True, blank=True)
    note2 = models.CharField(max_length=255, verbose_name='附件说明', null=True, blank=True)
    note3 = models.CharField(max_length=255, verbose_name='附件说明', null=True, blank=True)
    note4 = models.CharField(max_length=255, verbose_name='附件说明', null=True, blank=True)
    note5 = models.CharField(max_length=255, verbose_name='附件说明', null=True, blank=True)
    note6 = models.CharField(max_length=255, verbose_name='附件说明', null=True, blank=True)
    note7 = models.CharField(max_length=255, verbose_name='附件说明', null=True, blank=True)
    note8 = models.CharField(max_length=255, verbose_name='附件说明', null=True, blank=True)
    note9 = models.CharField(max_length=255, verbose_name='附件说明', null=True, blank=True)
    switch0 = models.IntegerField(verbose_name='是否启用', default=0)
    switch1 = models.IntegerField(verbose_name='是否启用', default=0)
    switch2 = models.IntegerField(verbose_name='是否启用', default=0)
    switch3 = models.IntegerField(verbose_name='是否启用', default=0)
    switch4 = models.IntegerField(verbose_name='是否启用', default=0)
    switch5 = models.IntegerField(verbose_name='是否启用', default=0)
    switch6 = models.IntegerField(verbose_name='是否启用', default=0)
    switch7 = models.IntegerField(verbose_name='是否启用', default=0)
    switch8 = models.IntegerField(verbose_name='是否启用', default=0)
    switch9 = models.IntegerField(verbose_name='是否启用', default=0)
    must0 = models.IntegerField(verbose_name='是否必须', default=0)
    must1 = models.IntegerField(verbose_name='是否必须', default=0)
    must2 = models.IntegerField(verbose_name='是否必须', default=0)
    must3 = models.IntegerField(verbose_name='是否必须', default=0)
    must4 = models.IntegerField(verbose_name='是否必须', default=0)
    must5 = models.IntegerField(verbose_name='是否必须', default=0)
    must6 = models.IntegerField(verbose_name='是否必须', default=0)
    must7 = models.IntegerField(verbose_name='是否必须', default=0)
    must8 = models.IntegerField(verbose_name='是否必须', default=0)
    must9 = models.IntegerField(verbose_name='是否必须', default=0)




    '''
    bldx = models.CharField(verbose_name='办理对象', max_length=255)
    znbm = models.CharField(max_length=255, null=True,blank=True, verbose_name='职能类别')
    dccs = models.IntegerField(default=1,verbose_name='到场次数')
    zgbm = models.CharField(max_length=255, verbose_name='主管部门',default='')
    sljg = models.CharField(max_length=255, verbose_name='受理机构', default='')
    slyj = models.TextField(verbose_name='设立依据', default='')
    bltj = models.TextField(verbose_name='办理条件', default='')
    sfsf = models.BooleanField(default=False, verbose_name='是否收费')
    sfyj = models.TextField(verbose_name='收费依据')
    fdqx = models.CharField(max_length=255, verbose_name='法定期限', default='5个工作日')
    clqx = models.CharField(max_length=255, verbose_name='承诺期限', default='5个工作日')
    # 办事办理流程
    #
    '''
    content = models.TextField(verbose_name='事项内容')
    handle = models.CharField(max_length=255, verbose_name='网上申办', default='否')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['type']
        verbose_name = '事项'
        verbose_name_plural = '事项'



'''
1、建立一个办事订单，连通微信用户和事项。
2、中间项还要包含附件（动态添加图片）；
---直接用富文本编辑器一步到位，只开放多图片上传的栏目。
---添加图片序列，用逗号来分开路劲。
创建日期；办结日期；
订单状态（预约-受理-发送模板信息-办结）；
评价内容；评价等级；

'''


class toShiXiang(models.Model):
    shixiang = models.ForeignKey(ShiXiang, verbose_name='办理事项')
    user = models.ForeignKey(BUser, verbose_name='办理人员',null=True)
    backcontent = models.TextField(verbose_name='反馈意见', null=True, default='接受办理申请。')
    state = models.CharField(max_length=125, verbose_name='事项状态', default='接受')
    comment = models.TextField(verbose_name='评论',default='',null=True)
    rank = models.CharField(max_length=64,verbose_name='评论等级', default='好')
    wechatuser = models.ForeignKey(BWechatUser, verbose_name='申请人员')
    senddata = models.TextField(verbose_name='申请资料')
    addtime = models.DateTimeField(auto_now_add=True, verbose_name='申请时间')
    xiugaitime = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    hold0 = models.CharField(max_length=255, null=True, blank=True, verbose_name='保留字段0')
    hold1 = models.CharField(max_length=255, null=True, blank=True, verbose_name='保留字段1')
    hold2 = models.CharField(max_length=255, null=True, blank=True, verbose_name='保留字段2')
    holdtime0 = models.DateTimeField(verbose_name='保留时间字段0', null=True, blank=True)

    file0 = models.FileField(upload_to='WebWork/', verbose_name='附件', default='',null=True, blank=True)
    file1 = models.FileField(upload_to='WebWork/', verbose_name='附件', default='',null=True, blank=True)
    file2 = models.FileField(upload_to='WebWork/', verbose_name='附件', default='',null=True, blank=True)
    file3 = models.FileField(upload_to='WebWork/', verbose_name='附件', default='',null=True, blank=True)
    file4 = models.FileField(upload_to='WebWork/', verbose_name='附件', default='',null=True, blank=True)
    file5 = models.FileField(upload_to='WebWork/', verbose_name='附件', default='',null=True, blank=True)
    file6 = models.FileField(upload_to='WebWork/', verbose_name='附件', default='',null=True, blank=True)
    file7 = models.FileField(upload_to='WebWork/', verbose_name='附件', default='',null=True, blank=True)
    file8 = models.FileField(upload_to='WebWork/', verbose_name='附件', default='',null=True, blank=True)
    file9 = models.FileField(upload_to='WebWork/', verbose_name='附件', default='',null=True, blank=True)
    note0 = models.CharField(max_length=255, verbose_name='附件说明', null=True, blank=True)
    note1 = models.CharField(max_length=255, verbose_name='附件说明', null=True, blank=True)
    note2 = models.CharField(max_length=255, verbose_name='附件说明', null=True, blank=True)
    note3 = models.CharField(max_length=255, verbose_name='附件说明', null=True, blank=True)
    note4 = models.CharField(max_length=255, verbose_name='附件说明', null=True, blank=True)
    note5 = models.CharField(max_length=255, verbose_name='附件说明', null=True, blank=True)
    note6 = models.CharField(max_length=255, verbose_name='附件说明', null=True, blank=True)
    note7 = models.CharField(max_length=255, verbose_name='附件说明', null=True, blank=True)
    note8 = models.CharField(max_length=255, verbose_name='附件说明', null=True, blank=True)
    note9 = models.CharField(max_length=255, verbose_name='附件说明', null=True, blank=True)

    def __str__(self):
        return '%s申请%s'%(self.wechatuser, self.shixiang)

    class Meta:
        verbose_name = '事项申请'
        verbose_name_plural = verbose_name
