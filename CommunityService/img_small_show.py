# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import os
import uuid
import json
import datetime as dt
from PIL import Image


#目录创建
def upload_generation_dir(dir_name):
    today = dt.datetime.today()
    dir_name = dir_name + '/%d/%d/' %(today.year,today.month)
    if not os.path.exists(settings.MEDIA_ROOT):
        os.makedirs(settings.MEDIA_ROOT)
    return dir_name

@csrf_exempt
def upload_image(request, dir_name):
    ##################
    #  Eleditor图片上传返回数据格式说明：
    # {"status": 1, "url": ""}
    # {"status": 0, "msg": "失败的提示"}
    ##################
    print("start upload img")
    result = {"status": 0, "message": "上传出错"}
    files = request.FILES.get("imgFile", None)
    if files:
        result = img_small_creat(files)
    return HttpResponse(json.dumps(result), content_type="application/json")


def img_small_creat(files):
    try:
        img = Image.open(files)
        # 图像缩小三倍
        width, height = img.size
        smallimg = img.resize((int(width / 3), int(height / 3)))

        # 获取图像的类型
        file_suffix = img.format

        # 创建目录
        relative_path_file = upload_generation_dir(dir_name)
        path = os.path.join(settings.MEDIA_ROOT, relative_path_file)
        if not os.path.exists(path):  # 如果目录不存在创建目录
            os.makedirs(path)
        # uuid就是生成一个随机的码
        file_name = str(uuid.uuid1()) + "." + file_suffix
        path_file = os.path.join(path, file_name)  # 这个是保存文件的路径
        file_url = settings.MEDIA_URL + relative_path_file + file_name  # 这个是返回给前端的路径
        # 保存压缩后的图像
        smallimg.save(path_file)
        # 设置返回结果
        return {"status": 1, "url": file_url}
    except:
        return {"status": 0, "msg": "图片压缩错误"}