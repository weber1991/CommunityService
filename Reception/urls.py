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
from Reception.views import *

app_name='Reception'
urlpatterns = [
    url(r'^$', communityshow, name='index'),
    url(r'^login/$', login, name='login'),
    url(r'^register/$', register, name='register'),
    url(r'^backpassowrd/$', backpassword, name='backpassword'),
    url(r'^need_register/$', need_register, name='need_register'),


    url(r'^myindex/$', myindex, name='myindex'),
    url(r'^mydata/$', mydata, name='mydata'),
    url(r'^mymessage/$', mymessage, name='mymessage'),
    url(r'^myshixiang/$', myshixiang, name='myshixiang'),
    url(r'^mytoshixiang/(?P<id>[0-9]+)/$', mytoshixiang, name='mytoshixiang'),
    url(r'^mytoshixiang_assess/(?P<id>[0-9]+)/$', mytoshixiang_assess, name='mytoshixiang_assess'),
    url(r'^myticket/$', myticket, name='myticket'),


    url(r'^communityshow/$', communityshow, name='communityshow'),
    url(r'^contactus/', contactus, name='contactus'),
    url(r'^showblog/', showblog, name='showblog'),
    url(r'^getblog/(?P<blogno>[0-9]+)/$', getblog, name='getblog'),


    url(r'^showshixiangtype/', showshixiangtype, name='showshixiangtype'),
    url(r'^showshixiang/(?P<typeid>[0-9]+)/$', showshixiang, name='showshixiang'),
    url(r'^getshixiang/(?P<bh>[0-9]+)/$', getshixiang, name='getshixiang'),
    url(r'^setshixiang/(?P<bh>[0-9]+)/$', setshixiang, name='setshixiang'),


    url(r'^setmessage/', setmessage, name='setmessage'),
    url(r'^showmessage/', showmessage, name='showmessage'),
    url(r'^getmessage/(?P<id>[0-9]+)/$', getmessage, name='getmessage'),

    url(r'^ticket_wait/$', ticket_wait, name='ticket_wait'),
    url(r'^ticket_get/$', ticket_get, name='ticket_get'),
    url(r'^ticket_appoint/$', ticket_appoint, name='ticket_appoint'),
    url(r'^ticket_show/$', ticket_show, name='ticket_show'),

    url(r'^random_check/$', random_check, name='random_check'),

    url(r'^ticket_assess/$', bticket_assess, name='bticket_assess'),

    url(r'^ticket_get_pc/dcpdfjhhwegugwit-iewjiejq/$', ticket_get_pc, name='ticket_get_pc'),
]
