from django import template

register = template.Library()

@register.filter
def Bstate_change(value):
    if value == 0:
        return '等候'
    if value == 1:
        return '在办理'
    if value == 2:
        return '已办结'
    if value == 3:
        return '已作废'
    if value == 4:
        return '预约-待审核'
    else:
        return None

@register.filter
def User_power(value):
    if value == 0:
        return '没有次权限'
    if value == 1:
        return '办事员'
    if value == 2:
        return '管理员'
    return 'error'