"""CommunityService URL Configuration

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
from django.contrib import admin
from CommunityService.settings import MEDIA_ROOT
from django.views.static import serve
from CommunityService.upload import *
from Reception.views import *
from CommunityService import eleditor_upload
from CommunityService import img_small_show


urlpatterns = [
    url(r'^$', communityshow),
    url(r'MP_verify_fphvDWPkwRt4yvpp.txt', wechaturlpower, name='wechaturlpower'),
    url(r'^admin/', admin.site.urls),
    # url(r'^media/Reception/(?P<path>.*)$',img_small_show.img_small),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
    url(r'^badmin/', include('BAdmin.urls')),
    url(r'^Reception/', include('Reception.urls')),
    # 配置kindeditor，这里是配置路由
    url(r'^admin/uploads/(?P<dir_name>[^/]+)$', upload_image, name='upload_image'),
    url(r'^Eleditor_uploads/(?P<dir_name>[^/]+)$', eleditor_upload.upload_image, name='eleditor_upload_img'),
    url(r'^Eleditor_small_uploads/(?P<dir_name>[^/]+)$', img_small_show.upload_image, name='eleditor_small_upload_img'),
    url(r"^uploads/(?P<path>.*)$", serve, {"document_root": MEDIA_ROOT, }),
]
