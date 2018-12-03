
# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import os
import uuid
import json
import datetime as dt
from PIL import Image


'''
1、这部分用来给文本编辑器调用
2、需要结合相应的url解析来使用
'''
@csrf_exempt
def upload_file(request, dir_name):
    ##################
    #  Eleditor图片上传返回数据格式说明：
    # {"status": 1, "url": ""}
    # {"status": 0, "msg": "失败的提示"}
    ##################
    print("start upload img")
    result = {"status": 0, "message": "上传出错"}
    files = request.FILES.get("imgFile", None)
    if files:
        result =file_upload(files, dir_name)  # 原版代码
    return HttpResponse(json.dumps(result), content_type="application/json")

# 目录创建
def upload_generation_dir(dir_name):
    today = dt.datetime.today()
    dir_name = dir_name + '/%d/%d/' %(today.year,today.month)
    if not os.path.exists(settings.MEDIA_ROOT):
        os.makedirs(settings.MEDIA_ROOT)
    return dir_name

# 文件上传，通过允许上传的文件类型来进行过滤
def file_upload(files, dir_name):
    # 允许上传文件类型
    allow_suffix =['jpg', 'png', 'jpeg', 'gif', 'bmp', 'zip', "swf", "flv",
                   "mp3", "wav", "wma", "wmv", "mid", "avi", "mpg", "asf",
                   "rm", "rmvb", "doc", "docx", "xls", "xlsx", "ppt", "htm",
                   "html", "txt", "zip", "rar", "gz" , "bz2" ]
    file_suffix = files.name.split(".")[-1]  # 获取文件类型
    if file_suffix not in allow_suffix:
        return {"status": 0,"error": 1, "message": "文件格式不正确"}
    file_name_show = files.name.split(".")[0]  # 获取文件名称
    relative_path_file = upload_generation_dir(dir_name)
    path=os.path.join(settings.MEDIA_ROOT, relative_path_file)
    if not os.path.exists(path):  # 如果目录不存在创建目录
        os.makedirs(path)
    file_name=str(uuid.uuid1())+"."+file_suffix
    path_file=os.path.join(path, file_name)
    file_url = settings.MEDIA_URL + relative_path_file + file_name
    open(path_file, 'wb').write(files.file.read())
    print(file_url)
    return {"status": 1, "url": file_url,"name":file_name_show}