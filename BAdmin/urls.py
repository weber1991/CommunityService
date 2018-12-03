"""xxbSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from BAdmin.views import *

app_name='BAdmin'
urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^blogin/', blogin, name='blogin'),
    url(r'index/$', index, name='index'),
    url(r'^comnunity_beditor/', community_beditor, name='comnunity_beditor'),
    url(r'^blogout/', blogout, name='blogout'),
    url(r'^contactus_beditor/', contactus_beditor, name='contactus_beditor'),
    url(r'^becomevolunteer_beditor/$', becomevolunteer_editor, name='becomevolunteer_editor'),

    url(r'^blog_add/', blog_add, name='blog_add'),
    url(r'^blog_editor/', blog_editor, name='blog_editor'),
    url(r'^blog_list/', blog_list, name='blog_list'),
    url(r'^blog_delete/(?P<blogno>[0-9]+)/$', blog_delete, name='blog_delete'),
    url(r'^blog_change/(?P<blogno>[0-9]+)/$', blog_change, name='blog_change'),
    url(r'^blog_data/(?P<blogno>[0-9]+)/$', blog_data, name='blog_data'),

    url(r'^shixiang_type/', shixiang_type, name='shixiang_type'),
    url(r'^shixiangtype_delete/(?P<shixiangtypeno>[0-9]+)/$', shixiangtype_delete, name='shixiangtype_delete'),
    url(r'^shixiang_add/', shixiang_add, name='shixiang_add'),
    url(r'^shixiang_list/', shixiang_list, name='shixiang_list'),
    url(r'^shixiang_change/(?P<bh>[0-9]+)/$',shixiang_change, name='shixiang_change'),
    url(r'^shixiang_handle/(?P<bh>[0-9]+)/$',shixiang_handle, name='shixiang_handle'),
    url(r'^shixiang_data/(?P<bh>[0-9]+)/$', shixiang_data, name='shixiang_data'),
    url(r'^shixiang_delete/(?P<bh>[0-9]+)/$', shixiang_delete, name='shixiang_delete'),

    # url(r'^message_process/(?P<bh>[0-9]+)/$', shixiang_delete, name='shixiang_delete'),
    url(r'^message_list/', message_list, name='message_list'),
    url(r'^message_all_list/', message_all_list, name='message_all_list'),
    url(r'^message_set_list/', message_set_list, name='message_set_list'),
    url(r'^message_set/(?P<messageid>[0-9]+)/', message_set, name='message_set'),
    url(r'^message_change/(?P<messageid>[0-9]+)/', message_change, name='message_change'),
    url(r'^message_back/(?P<messageid>[0-9]+)/', message_back, name='message_back'),
    url(r'^message_check_list/', message_check_list, name='message_check_list'),
    url(r'^message_check/(?P<messageid>[0-9]+)/', message_check, name='message_check'),
    url(r'^message_look/(?P<messageid>[0-9]+)/', message_look, name='message_look'),


    url(r'^toshixiang_list/$', toshixiang_list, name='toshixiang_list'),
    url(r'^toshixiang_list_all/$', toshixiang_list_all, name='toshixiang_list_all'),
    url(r'^toshixiang_setlist/$', toshixiang_setlist, name='toshixiang_setlist'),
    url(r'^toshixiang_editor/(?P<id>[0-9]+)/$', toshixiang_editor, name='toshixiang_editor'),
    url(r'^toshixiang_set/(?P<id>[0-9]+)/$', toshixiang_set, name='toshixiang_set'),

    url(r'^service_add', serviece_add, name='service_add'),
    url(r'^service_list', service_list, name='service_list'),
    url(r'^service_editor/(?P<id>[0-9]+)/$', service_editor, name='service_editor'),
    url(r'^service_delete/(?P<id>[0-9]+)/$', service_delete, name='service_delete'),
    url(r'^service_change/(?P<id>[0-9]+)/$', service_change, name='service_change'),

    url(r'^ticket_list/$', ticket_list, name='ticket_list'),
    url(r'^ticket_list_all/$', ticket_list_all, name='ticket_list_all'),
    url(r'^ticket_appoint/$', ticket_appoint, name='ticket_appoint'),
    url(r'^ticket_start/(?P<id>[0-9]+)/$', ticket_start, name='ticket_start'),
    url(r'^ticket_doing/(?P<id>[0-9]+)/$', ticket_doing, name='ticket_doing'),
    url(r'^ticket_end/(?P<id>[0-9]+)/$', ticket_end, name='ticket_end'),
    url(r'^ticket_out/(?P<id>[0-9]+)/$', ticket_out, name='ticket_out'),
    url(r'^ticket_next/$', ticket_next, name='ticket_next'),
    url(r'^call_back/$', call_back, name='call_back'),

    url(r'^user2window/$', window_2_user, name='window_2_user'),
    url(r'^window_list/$', window_list, name='window_list'),
    url(r'window_delete/(?P<id>[0-9]+)/$', window_delete, name='window_delete'),

    url(r'^random_list/$', random_list, name='random_list'),
    url(r'^random_delete/(?P<id>[0-9]+)/$', random_delete, name='random_delete'),
    url(r'^random_change/(?P<id>[0-9]+)/$', random_change, name='random_change'),

    url(r'^user_data/(?P<id>[0-9]+)/$', user_data, name='user_data'),
    url(r'^user_list/$', user_list, name='user_list'),
    url(r'^user_delete/(?P<id>[0-9]+)/$', user_delete, name='user_delete'),
    url(r'^user_set/(?P<id>[0-9]+)/$', user_set, name='user_set'),

    url(r'^wechatuser_list/$', wechatuser_list, name='wechatuser_list'),
    url(r'^wechatuser_delete/(?P<id>[0-9]+)/$', wechatuser_delete, name='wechatuser_delete'),

]
