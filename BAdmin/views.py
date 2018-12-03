from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from BUser.models import *
from BAdmin.models import *
from Blog.models import *
from WebWork.models import *
from django.contrib import sessions
from Message.models import *
from Ticket.models import *
import datetime
from CommunityService.file_upload import *
from CommunityService import settings
# Create your views here.



def blogin(req):
    if req.method == 'GET':
        return render(req, 'BAdmin/login.html', {})
    else:
        name = req.POST.get('username')
        password = req.POST.get('password')
        user = BUser.objects.filter(name=name, password=password).first()
        if user:
            req.session['username'] = name
            return redirect('/badmin/index')
        else:
            return render(req, 'BAdmin/login.html', {'msg':'用户名/密码错误'})


def blogout(req):
    req.session['username'] = ''
    return redirect('BAdmin:blogin')


def index(req):
    username = req.session.get('username',None)
    if username is None:
        return redirect('/badmin/blogin')
    else:
        user = BUser.objects.get(username=username)
        return render(req, 'BAdmin/index.html', {'user':user})


def community_beditor(req):
    communitydata = CommunityBase.objects.get(id=1)
    if req.method == 'GET':
        if communitydata is None:
            communitydata = CommunityBase.objects.create(id=1, title = '社区信息', content='社区简介', author='发布人')
            return render(req, 'BAdmin/community_beditor.html', {'communitydata': communitydata})
    else:
        title = req.POST.get('met_title')
        content = req.POST.get('met_content')
        author = req.POST.get('met_author')
        communitydata.title = title
        communitydata.content = content
        communitydata.author = author
        communitydata.save()
    return render(req, 'BAdmin/community_beditor.html', {'communitydata': communitydata})


def contactus_beditor(req):
    contactus = CommunityBase.objects.get(id=2)
    if req.method == 'GET':
        if contactus is None:
            contactus = CommunityBase.objects.create(id=2, title = '联系我们', content='内容', author='管理员')
            return render(req, 'BAdmin/contactus_beditor.html', {'contactus': contactus})
    else:
        author = req.POST.get('met_author')
        content = req.POST.get('met_content')
        contactus.author = author
        contactus.content = content
        contactus.save()
    return render(req, 'BAdmin/contactus_beditor.html', {'contactus': contactus})


def becomevolunteer_editor(req):
    volunteer = CommunityBase.objects.get(id=3)
    if req.method == 'GET':
        if volunteer is None:
            volunteer = CommunityBase.objects.create(id=3, title = '志愿者', content='内容', author='管理员')
    else:
        author = req.POST.get('met_author')
        content = req.POST.get('met_content')
        volunteer.author = author
        volunteer.content = content
        volunteer.save()
    return render(req, 'BAdmin/volunteer_beditor.html', {'volunteer': volunteer})


def blog_add(req):
    if req.method == 'GET':
        return render(req, 'BAdmin/blog_add.html',{})
    else:
        title = req.POST.get('met_title')
        content = req.POST.get('met_content')
        author = req.POST.get('met_author')
        desc = req.POST.get('met_desc')
        blog = Article.objects.create(title=title, user=author, desc=desc, content=content, state='草稿')
        return redirect('BAdmin:blog_list')

def blog_editor(req):
    if req.method == 'GET':

        return render(req, 'BAdmin/blog_beditor.html',{})
    else:
        title = req.POST.get('met_title')
        content = req.POST.get('met_content')
        author = req.POST.get('met_author')
        return render(req, 'BAdmin/blog_beditor.html',{})


def blog_list(req):
    if req.method == 'GET':
        bloglist = Article.objects.all()
        return render(req, 'BAdmin/blog_list.html',{'bloglist':bloglist})

def blog_delete(req, blogno):
    blog = Article.objects.get(id = blogno).delete()
    return redirect('BAdmin:blog_list')

def blog_change(req, blogno):
    blog = Article.objects.get(id = blogno)
    if blog.state == '草稿':
        blog.state = '发布'
        blog.save()
    else:
        blog.state = '草稿'
        blog.save()
    return redirect('BAdmin:blog_list')

def blog_data(req, blogno):
    blog = Article.objects.get(id=blogno)
    if req.method == 'GET':
        return render(req, 'BAdmin/blog_data.html', {'blog': blog})
    else:
        blog.title = req.POST.get('met_title')
        blog.content = req.POST.get('met_content')
        blog.user = req.POST.get('met_author')
        blog.desc = req.POST.get('met_desc')
        blog.save()
        return redirect('BAdmin:blog_list')

def shixiang_type(req):
    if req.method == 'GET':
        shixiangtypelist = ShiXiangType.objects.all()
        return render(req, 'BAdmin/shixiangType_editor.html',{'shixiangtypelist':shixiangtypelist})
    else:
        typename = req.POST.get('met_typename', None)
        if typename is not None:
            ShiXiangType.objects.create(name=typename)
        shixiangtypelist = ShiXiangType.objects.all()
        return render(req, 'BAdmin/shixiangType_editor.html', {'shixiangtypelist': shixiangtypelist})

def shixiangtype_delete(req, shixiangtypeno):
    type = ShiXiangType.objects.filter(id = shixiangtypeno).delete()
    return redirect('BAdmin:shixiang_type')

def shixiang_add(req):
    if req.method == 'GET':
        shixiangtypelist = ShiXiangType.objects.all()
        return render(req, 'BAdmin/shixiang_add.html', {'shixiangtypelist':shixiangtypelist})
    else:
        name = req.POST.get('met_name', None)
        type = req.POST.get('met_type', None)
        content = req.POST.get('met_content', None)
        shixiangtype = ShiXiangType.objects.get(id = type)
        shixiang = ShiXiang.objects.create(name=name, type=shixiangtype, content=content, sxzt='草稿')


        # 2018-10-16修改
        # 以noteX为主要，为上传资料，然后fileX为辅助，有则上传，保存为路径，无则用javascript:;来保存。
        # ---更优化思维1，理论上不限上传文件个数，用一个字段来记存所有文件路径和名字
        # ---更优化思维2，用一对多关系，绑定多个文件+文件名的modle
        # 2018-10-17修改
        # 不写成javascript;
        note0 = req.POST.get("filename0", None)
        file0 = req.FILES.get("file0", None)
        if note0:
            shixiang.note0 = note0
        if file0:
            switch0 = req.POST.get("switch0",0)
            must0 = req.POST.get("must0", 0)
            shixiang.switch0 = int(switch0)
            shixiang.must0 = int(must0)
            upload_answer0 = file_upload(file0, 'WebWord')
            print(upload_answer0)
            if upload_answer0["status"] == 1:
                shixiang.file0 = upload_answer0["url"]
                # shixiang.note0 = upload_answer0["name"]


        note1 = req.POST.get("filename1", None)
        if note1:
            shixiang.note1 = note1
        file1 = req.FILES.get("file1", None)
        if file1:
            switch1 = req.POST.get("switch1",0)
            must1 = req.POST.get("must1", 0)
            shixiang.switch1 = int(switch1)
            shixiang.must1 = int(must1)
            upload_answer1 = file_upload(file1, 'WebWord')
            if upload_answer1["status"] == 1:
                shixiang.file1 = upload_answer1["url"]
                # shixiang.note1 = upload_answer1["name"]


        note2 = req.POST.get("filename2", None)
        if note2:
            shixiang.note2 = note2
        file2 = req.FILES.get("file2", None)
        if file2:
            switch2 = req.POST.get("switch2",0)
            must2 = req.POST.get("must2", 0)
            shixiang.switch2 = int(switch2)
            shixiang.must2 = int(must2)
            upload_answer2 = file_upload(file2, 'WebWord')
            if upload_answer2["status"] == 1:
                shixiang.file2 = upload_answer2["url"]
                # shixiang.note2 = upload_answer2["name"]


        note3 = req.POST.get("filename3", None)
        if note3:
            shixiang.note3 = note3
        file3 = req.FILES.get("file3", None)
        if file3:
            switch3 = req.POST.get("switch3",0)
            must3 = req.POST.get("must3", 0)
            shixiang.switch3 = int(switch3)
            shixiang.must3 = int(must3)
            upload_answer3 = file_upload(file3, 'WebWord')
            if upload_answer3["status"] == 1:
                shixiang.file3 = upload_answer3["url"]
                # shixiang.note3 = upload_answer3["name"]


        note4 = req.POST.get("filename4", None)
        if note4:
            shixiang.note4 = note4
        file4 = req.FILES.get("file4", None)
        if file4:
            switch4 = req.POST.get("switch4",0)
            must4 = req.POST.get("must4", 0)
            shixiang.switch4 = int(switch4)
            shixiang.must4 = int(must4)
            upload_answer4 = file_upload(file4, 'WebWord')
            if upload_answer4["status"] == 1:
                shixiang.file4 = upload_answer4["url"]
                # shixiang.note4 = upload_answer4["name"]


        note5 = req.POST.get("filename5", None)
        if note5:
            shixiang.note5 = note5
        file5 = req.FILES.get("file5", None)
        if file5:
            switch5 = req.POST.get("switch5",0)
            must5 = req.POST.get("must5", 0)
            shixiang.switch5 = int(switch5)
            shixiang.must5 = int(must5)
            upload_answer5 = file_upload(file5, 'WebWord')
            if upload_answer5["status"] == 1:
                shixiang.file5 = upload_answer5["url"]
                # shixiang.note5 = upload_answer5["name"]


        note6 = req.POST.get("filename6", None)
        if note6:
            shixiang.note6 = note6
        file6 = req.FILES.get("file6", None)
        if file6:
            switch6 = req.POST.get("switch6",0)
            must6 = req.POST.get("must6", 0)
            shixiang.switch6 = int(switch6)
            shixiang.must6 = int(must6)
            upload_answer6 = file_upload(file6, 'WebWord')
            if upload_answer6["status"] == 1:
                shixiang.file6 = upload_answer6["url"]
                # shixiang.note6 = upload_answer6["name"]


        note7 = req.POST.get("filename7", None)
        if note7:
            shixiang.note7 = note7
        file7 = req.FILES.get("file7", None)
        if file7:
            switch7 = req.POST.get("switch7",0)
            must7 = req.POST.get("must7", 0)
            shixiang.switch7 = int(switch7)
            shixiang.must7 = int(must7)
            upload_answer7 = file_upload(file7, 'WebWord')
            if upload_answer7["status"] == 1:
                shixiang.file7 = upload_answer7["url"]
                # shixiang.note7 = upload_answer7["name"]



        note8 = req.POST.get("filename8", None)
        if note8:
            shixiang.note8 = note8
        file8 = req.FILES.get("file8", None)
        if file8:
            switch8 = req.POST.get("switch8",0)
            must8 = req.POST.get("must8", 0)
            shixiang.switch8 = int(switch8)
            shixiang.must8 = int(must8)
            upload_answer8 = file_upload(file8, 'WebWord')
            if upload_answer8["status"] == 1:
                shixiang.file8 = upload_answer8["url"]
                # shixiang.note8 = upload_answer8["name"]


        note9 = req.POST.get("filename9", None)
        if note9:
            shixiang.note9 = note9
        file9 = req.FILES.get("file9", None)
        if file9:
            switch9 = req.POST.get("switch9",0)
            must9 = req.POST.get("must9", 0)
            shixiang.switch9 = int(switch9)
            shixiang.must9 = int(must9)
            upload_answer9 = file_upload(file9, 'WebWord')
            if upload_answer9["status"] == 1:
                shixiang.file9 = upload_answer9["url"]
                # shixiang.note9 = upload_answer9["name"]

        shixiang.save()

        return redirect('BAdmin:shixiang_list')


def shixiang_list(req):
    if req.method == 'GET':
        shixianglist = ShiXiang.objects.all()
        return render(req, 'BAdmin/shixiang_list.html', {'shixianglist':shixianglist})


def shixiang_data(req, bh):
    shixiang = ShiXiang.objects.get(bh = bh)
    shixiangtypelist = ShiXiangType.objects.all()
    print('!!!!!')
    print(shixiang.file2)
    print('!!!!!')
    if req.method == 'GET':
        return render(req, 'BAdmin/shixiang_data.html', {'shixiang': shixiang, 'shixiangtypelist': shixiangtypelist})
    else:
        shixiang.name = req.POST.get('met_name', None)
        type = req.POST.get('met_type', None)
        shixiangtype = ShiXiangType.objects.get(id=type)
        shixiang.type = shixiangtype
        shixiang.content = req.POST.get('met_content', None)
        switch0 = req.POST.get("switch0", 0)
        must0 = req.POST.get("must0", 0)
        switch1 = req.POST.get("switch1", 0)
        must1 = req.POST.get("must1", 0)
        switch2 = req.POST.get("switch2", 0)
        must2 = req.POST.get("must2", 0)
        switch3 = req.POST.get("switch3", 0)
        must3 = req.POST.get("must3", 0)
        switch4 = req.POST.get("switch4", 0)
        must4 = req.POST.get("must4", 0)
        switch5 = req.POST.get("switch5", 0)
        must5 = req.POST.get("must5", 0)
        switch6 = req.POST.get("switch6", 0)
        must6 = req.POST.get("must6", 0)
        switch7 = req.POST.get("switch7", 0)
        must7 = req.POST.get("must7", 0)
        switch8 = req.POST.get("switch8", 0)
        must8 = req.POST.get("must8", 0)
        switch9 = req.POST.get("switch9", 0)
        must9 = req.POST.get("must9", 0)
        shixiang.switch0 = int(switch0)
        shixiang.must0 = int(must0)
        shixiang.switch1 = int(switch1)
        shixiang.must1 = int(must1)
        shixiang.switch2 = int(switch2)
        shixiang.must2 = int(must2)
        shixiang.switch3 = int(switch3)
        shixiang.must3 = int(must3)
        shixiang.switch4 = int(switch4)
        shixiang.must4 = int(must4)
        shixiang.switch5 = int(switch5)
        shixiang.must5 = int(must5)
        shixiang.switch6 = int(switch6)
        shixiang.must6 = int(must6)
        shixiang.switch7 = int(switch7)
        shixiang.must7 = int(must7)
        shixiang.switch8 = int(switch8)
        shixiang.must8 = int(must8)
        shixiang.switch8 = int(switch8)
        shixiang.must8 = int(must8)
        shixiang.switch9 = int(switch9)
        shixiang.must9 = int(must9)


        note0 = req.POST.get("filename0", None)
        if note0:
            shixiang.note0 = note0
        file0 = req.FILES.get("file0", None)
        if file0:
            upload_answer0 = file_upload(file0, 'WebWord')
            print(upload_answer0)
            if upload_answer0["status"] == 1:
                shixiang.file0 = upload_answer0["url"]
                # shixiang.note0 = upload_answer0["name"]

        note1 = req.POST.get("filename1", None)
        if note1:
            shixiang.note1 = note1
        file1 = req.FILES.get("file1", None)
        if file1:
            upload_answer1 = file_upload(file1, 'WebWord')
            if upload_answer1["status"] == 1:
                shixiang.file1 = upload_answer1["url"]
                # shixiang.note1 = upload_answer1["name"]

        note2 = req.POST.get("filename2", None)
        if note2:
            shixiang.note2 = note2
        file2 = req.FILES.get("file2", None)
        if file2:
            upload_answer2 = file_upload(file2, 'WebWord')
            if upload_answer2["status"] == 1:
                shixiang.file2 = upload_answer2["url"]
                # shixiang.note2 = upload_answer2["name"]

        note3 = req.POST.get("filename3", None)
        if note3:
            shixiang.note3 = note3
        file3 = req.FILES.get("file3", None)
        if file3:
            upload_answer3 = file_upload(file3, 'WebWord')
            if upload_answer3["status"] == 1:
                shixiang.file3 = upload_answer3["url"]
                # shixiang.note3 = upload_answer3["name"]


        note4 = req.POST.get("filename4", None)
        if note4:
            shixiang.note4 = note4
        file4 = req.FILES.get("file4", None)
        if file4:
            upload_answer4 = file_upload(file4, 'WebWord')
            if upload_answer4["status"] == 1:
                shixiang.file4 = upload_answer4["url"]
                # shixiang.note4 = upload_answer4["name"]

        note5 = req.POST.get("filename5", None)
        if note5:
            shixiang.note5 = note5
        file5 = req.FILES.get("file5", None)
        if file5:
            upload_answer5 = file_upload(file5, 'WebWord')
            if upload_answer5["status"] == 1:
                shixiang.file5 = upload_answer5["url"]
                #shixiang.note5 = upload_answer5["name"]

        note6 = req.POST.get("filename6", None)
        if note6:
            shixiang.note6 = note6
        file6 = req.FILES.get("file6", None)
        if file6:
            upload_answer6 = file_upload(file6, 'WebWord')
            if upload_answer6["status"] == 1:
                shixiang.file6 = upload_answer6["url"]
                #shixiang.note6 = upload_answer6["name"]

        note7 = req.POST.get("filename7", None)
        if note7:
            shixiang.note7 = note7
        file7 = req.FILES.get("file7", None)
        if file7:
            upload_answer7 = file_upload(file7, 'WebWord')
            if upload_answer7["status"] == 1:
                shixiang.file7 = upload_answer7["url"]
                #shixiang.note7 = upload_answer7["name"]
        note8 = req.POST.get("filename8", None)
        if note8:
            shixiang.note8 = note8
        file8 = req.FILES.get("file8", None)
        if file8:
            upload_answer8 = file_upload(file8, 'WebWord')
            if upload_answer8["status"] == 1:
                shixiang.file8 = upload_answer8["url"]
                #shixiang.note8 = upload_answer8["name"]
        note9 = req.POST.get("filename9", None)
        if note9:
            shixiang.note9 = note9
        file9 = req.FILES.get("file9", None)
        if file9:
            upload_answer9 = file_upload(file9, 'WebWord')
            if upload_answer9["status"] == 1:
                shixiang.file9 = upload_answer9["url"]
                #shixiang.note9 = upload_answer9["name"]
        shixiang.sxzt = '草稿'
        shixiang.save()
        return redirect('BAdmin:shixiang_list')


def shixiang_delete(req, bh):
    shixiang = ShiXiang.objects.filter(bh=bh).delete()
    return redirect('BAdmin:shixiang_list')


def shixiang_change(req, bh):
    shixiang = ShiXiang.objects.get(bh=bh)
    if shixiang.sxzt == '草稿':
        shixiang.sxzt = '发布'
    else:
        shixiang.sxzt = '草稿'
    shixiang.save()
    return redirect('BAdmin:shixiang_list')


def shixiang_handle(req, bh):
    shixiang = ShiXiang.objects.get(bh=bh)
    if shixiang.handle == '是':
        shixiang.handle = '否'
    else:
        shixiang.handle = '是'
    shixiang.save()
    return redirect('BAdmin:shixiang_list')


def message_set(req, messageid):
    message = Message.objects.get(id=messageid)
    if req.method == 'GET':
        userlist = BUser.objects.filter(message__gte=1)
        return render(req, 'BAdmin/message_set.html', {'userlist':userlist, 'message':message})
    else:
        # 获取传递过来的账号，用账号作唯一识别
        username = req.POST.get("met_backname", None)
        if username:
            message.backname = username
            message.process = '待回复'
            message.save()
        return redirect('BAdmin:message_set_list')


def message_set_list(req):
    message_list = Message.objects.filter(process='待分派')
    return render(req, 'BAdmin/message_set_list.html', {'messagelist':message_list})


# 需要做成我的list
def message_list(req):
    username = req.session.get('username', None)
    messagelist = Message.objects.filter(backname=username, process='待回复')
    return render(req, 'BAdmin/message_list.html', {'messagelist': messagelist})

def message_all_list(req):
    messagelist = Message.objects.all()
    return render(req, 'BAdmin/message_all_list.html', {'messagelist': messagelist})


def message_change(req, messageid):
    message = Message.objects.get(id = messageid)
    if message.state == '公开':
        message.state = '私密'
    elif message.state == '私密':
        message.state = '隐藏'
    else:
        message.state = '公开'
    message.save()
    return redirect('BAdmin:message_list')


def message_back(req, messageid):
    message = Message.objects.get(id = messageid)
    if req.method == 'GET':
        return render(req, 'BAdmin/message_back.html', {'message': message})
    if req.method == 'POST':
        backname = req.POST.get('met_backname', None)
        backcontent = req.POST.get('met_backcontent', None)
        print(backname, backcontent)
        if backname and backcontent:
            message.backname = backname
            message.backcontent = backcontent
            # message.process = '待发送'  # 微信用
            # message.process = '已回复' # 忽略审阅的步骤
            message.process = '待审阅'
            message.save()
        return redirect('BAdmin:message_list')
    return redirect('BAdmin:message_list')


def message_check_list(req):
    messagelist = Message.objects.filter(process='待审阅')
    return render(req, 'BAdmin/message_check_list.html', {'messagelist':messagelist})


def message_check(req, messageid):
    message = Message.objects.get(id=messageid)
    if req.method == 'GET':
        return render(req, 'BAdmin/message_check.html', { 'message':message})
    else:
        # 获取传递过来的账号，用账号作唯一识别
        check = req.POST.get("met_check", None)
        if check:
            message.process = check
            message.save()
        return redirect('BAdmin:message_check_list')


def message_look(req, messageid):
    message = Message.objects.get(id=messageid)
    if req.method == 'GET':
        return render(req, 'BAdmin/message_look.html', { 'message':message})

def toshixiang_list(req):
    username = req.session.get('username',None)
    if username is None:
        return redirect('/badmin/blogin')

    # 这里是筛选今天的事项，利用__get这个关键方法
    # import datetime
    # toshixianglist_today = toShiXiang.objects.filter(addtime__gte=datetime.date.today())
    # print(toshixianglist_today)

    user = BUser.objects.filter(name=username)
    toshixianglist_my = toShiXiang.objects.filter(user=user, state='待回复')
    # return render(req, 'BAdmin/toshixiang_list.html', {'toshixianglist_today':toshixianglist_today})

    return render(req, 'BAdmin/toshixiang_list.html', {'toshixianglist_my':toshixianglist_my})


def toshixiang_list_all(req):
    username = req.session.get('username',None)
    if username is None:
        return redirect('BAdmin:blogin')
    toshixianglist_all = toShiXiang.objects.all()
    print(toshixianglist_all)
    return render(req, 'BAdmin/toshixiang_list_all.html', {'toshixianglist_all':toshixianglist_all})


def toshixiang_editor(req, id):
    username = req.session.get('username',None)
    if username is None:
        return redirect('BAdmin:blogin')
    toshixiang = toShiXiang.objects.get(id = id)
    if req.method == 'GET':
        file_list = []
        if toshixiang.file0:
            temp = {'name':toshixiang.note0, 'url':toshixiang.file0}
            file_list.append(temp)
        if toshixiang.file1:
            temp = {'name':toshixiang.note0, 'url':toshixiang.file1}
            file_list.append(temp)
        if toshixiang.file2:
            temp = {'name':toshixiang.note0, 'url':toshixiang.file2}
            file_list.append(temp)
        if toshixiang.file3:
            temp = {'name':toshixiang.note0, 'url':toshixiang.file3}
            file_list.append(temp)
        if toshixiang.file4:
            temp = {'name':toshixiang.note0, 'url':toshixiang.file4}
            file_list.append(temp)
        if toshixiang.file5:
            temp = {'name':toshixiang.note0, 'url':toshixiang.file5}
            file_list.append(temp)
        if toshixiang.file6:
            temp = {'name':toshixiang.note0, 'url':toshixiang.file6}
            file_list.append(temp)
        if toshixiang.file7:
            temp = {'name':toshixiang.note0, 'url':toshixiang.file7}
            file_list.append(temp)
        if toshixiang.file8:
            temp = {'name':toshixiang.note0, 'url':toshixiang.file8}
            file_list.append(temp)
        if toshixiang.file9:
            temp = {'name':toshixiang.note0, 'url':toshixiang.file9}
            file_list.append(temp)
        return render(req, 'BAdmin/toshixiang_editor.html',
                      {'toshixiang':toshixiang,'file_list':file_list})
    else:
        backcontent = req.POST.get('met_backcontent', None)
        toshixiang.backcontent = backcontent
        back_answer = req.POST.get('met_backanswer')
        # 两种结果：要么退回，要么通过
        toshixiang.state = back_answer
        toshixiang.save()
        return redirect('BAdmin:toshixiang_list')




def toshixiang_setlist(req):
    username = req.session.get('username',None)
    if username is None:
        return redirect('BAdmin:blogin')
    toshixiangsetlist = toShiXiang.objects.filter(state='待分派')

    return render(req, 'BAdmin/toshixiang_setlist.html', {'toshixiangsetlist':toshixiangsetlist})



def toshixiang_set(req, id):
    username = req.session.get('username',None)
    if username is None:
        return redirect('BAdmin:blogin')

    toshixiang = toShiXiang.objects.get(id=id)
    file_list = []
    if toshixiang.note0 is not None:
        temp = {'name':toshixiang.note0, 'url':toshixiang.file0}
        file_list.append(temp)
    if toshixiang.note1 is not None:
        temp = {'name':toshixiang.note1, 'url':toshixiang.file1}
        file_list.append(temp)
    if toshixiang.note2 is not None:
        temp = {'name':toshixiang.note2, 'url':toshixiang.file2}
        file_list.append(temp)
    if toshixiang.note3 is not None:
        temp = {'name':toshixiang.note3, 'url':toshixiang.file3}
        file_list.append(temp)
    if toshixiang.note4 is not None:
        temp = {'name':toshixiang.note4, 'url':toshixiang.file4}
        file_list.append(temp)
    if toshixiang.note5 is not None:
        temp = {'name':toshixiang.note5, 'url':toshixiang.file5}
        file_list.append(temp)
    if toshixiang.note6 is not None:
        temp = {'name':toshixiang.note6, 'url':toshixiang.file6}
        file_list.append(temp)
    if toshixiang.note7 is not None:
        temp = {'name':toshixiang.note7, 'url':toshixiang.file7}
        file_list.append(temp)
    if toshixiang.note8 is not None:
        temp = {'name':toshixiang.note8, 'url':toshixiang.file8}
        file_list.append(temp)
    if toshixiang.note9 is not None:
        temp = {'name':toshixiang.note9, 'url':toshixiang.file9}
        file_list.append(temp)

    if req.method == 'GET':
        userlist = BUser.objects.filter(webword__gte=1)
        return render(req, 'BAdmin/toshixiang_set.html', {'toshixiang':toshixiang, 'userlist':userlist,
                                                          'file_list':file_list,}
                      )
    else:
        userid = req.POST.get('met_user', None)
        if userid:
            user = BUser.objects.get(id=userid)
            toshixiang.user = user
            toshixiang.state = '待回复'
            toshixiang.save()
            return redirect('BAdmin:toshixiang_list_all')
        else:
            return redirect('BAdmin:toshixiang_list_all')




def service_list(req):
    username = req.session.get('username',None)
    if username is None:
        return redirect('BAdmin:blogin')
    servicelist = BService.objects.all()
    return render(req, 'BAdmin/service_list.html',{'servicelist':servicelist})


def serviece_add(req):
    username = req.session.get('username',None)
    if username is None:
        return redirect('BAdmin:blogin')

    if req.method == 'GET':
        window_list = BWindow.objects.all()
        return render(req, 'BAdmin/service_add.html', {'window_list':window_list})
    else:
        name = req.POST.get('met_name', None)
        type = req.POST.get('met_type', None)
        window_list = req.POST.getlist('met_windows', '')
        print(window_list)
        note = req.POST.get('met_note', '')
        if name and type:
            service = BService.objects.create(
                name = name,
                type = type,
                #window = window,
                note = note,
                state='不支持'
            )
            # 还要创建业务和窗口的关系
            window_name = ''
            try:
                for window_id in window_list:
                    window = BWindow.objects.get(id = window_id)
                    window2service = BWindow2Service.objects.create(window = window, service=service)
                    window_name = window_name + window.name + ','
                service.window = window_name
                service.save()
            except:
                service.window = '无'
                service.save()
            return redirect('BAdmin:service_list')
        else:
            return redirect('BAdmin:service_add')


# 不做修改，只做删除和新增
def service_editor(req, id):
    username = req.session.get('username', None)
    if username is None:
        return redirect('BAdmin:blogin')

    service = BService.objects.get(id=id)
    if req.method == 'GET':
        return render(req, 'BAdmin/service_editor.html', {'service':service})
    else:
        name = req.POST.get('met_name', '')
        type = req.POST.get('met_type', '')
        window = req.POST.get('met_window', '')
        note = req.POST.get('met_note', '')
        service.name = name
        service.type = type
        service.window = window
        service.note = note
        service.state = '不支持'
        service.save()
        return redirect('BAdmin:service_list')


def service_delete(req, id):
    service = BService.objects.get(id=id).delete()
    return redirect('BAdmin:service_list')

def service_change(req, id):
    service = BService.objects.get(id = id)
    if service.state == '支持':
        service.state = '不支持'
        service.save()
    else:
        service.state = '支持'
        service.save()
    return redirect('BAdmin:service_list')


def ticket_list_all(req):
    username = req.session.get('username', None)
    if username is None:
        return redirect('BAdmin:blogin')
    pageDict = {}
    pageDict["allCount"] = BTicket.objects.count()
    pageDict["allPage"] = int(pageDict["allCount"]/settings.PAGECOUNT)
    if (pageDict["allCount"] % settings.PAGECOUNT) != 0:
        pageDict["allPage"] = pageDict["allPage"] + 1

    try:
        pageDict["nowPage"] = int(req.GET.get('nowPage', 1))
        pageDict["pageType"] = req.GET.get('pageType', '')
    except:
        pass

    if pageDict["pageType"] == 'next':
        pageDict["nowPage"] += 1
    if pageDict["pageType"] == 'last':
        pageDict["nowPage"] -= 1


    ticketlist_all = BTicket.objects.all().order_by('-addtime')[(pageDict["nowPage"]-1)*settings.PAGECOUNT:pageDict["nowPage"]*settings.PAGECOUNT]
    return render(req, 'BAdmin/ticket_list_all.html',
                  {'ticketlist_all': ticketlist_all,
                   'pageDict':pageDict,
                   })


def ticket_list(req):
    today = datetime.date.today()
    print(today)
    ticketdoinglist = BTicket.objects.filter(starttime__gte=today, state=1).order_by('starttime')
    ticketlist = BTicket.objects.filter(starttime__gte=today, state=0).order_by('starttime')
    return render(req, 'BAdmin/ticket_list.html', {'ticketlist':ticketlist, 'ticketdoinglist':ticketdoinglist})


def ticket_appoint(req):
    ticketappoint_list = BTicket.objects.filter(type=True, state=4).order_by('starttime')
    return render(req, 'BAdmin/ticket_appoint.html', {'ticketappoint_list':ticketappoint_list})

# 预约通过
def ticket_start(req, id):
    ticket = BTicket.objects.get(id = id)
    ticket.state = 0
    now = datetime.datetime.now()
    ticket.starttime = now
    ticket.save()
    return redirect('BAdmin:ticket_appoint')

# 呼号
def ticket_next(req):
    username = req.session.get('username', None)
    today = datetime.date.today()

    if username is None:
        return redirect('BAdmin:blogin')
    buser = BUser.objects.get(username=username)
    try:
        ticket_doing_end = BTicket.objects.filter(state=1, user=buser).first()
        ticket_doing_end.state = 2
        now = datetime.datetime.now()
        ticket_doing_end.endtime = now
        ticket_doing_end.save()
    except:
        pass

    #  保证语音
    # try:
    #     ticket_call_end_id = req.GET.get("ticketno", None)
    #     if ticket_call_end_id:
    #         ticket_call_end = BTicket.objects.get(id = ticket_call_end_id)
    #         ticket_call_end.hold0 = '0'
    #         ticket_call_end.save()
    # except:
    #     pass

    try:
        window2user = BUser2Window.objects.filter(user=buser).first()
    except:
        return redirect('BAdmin:window_2_user')

    window = window2user.window
    service2window_list = BWindow2Service.objects.filter(window=window)
    print('********')
    print(service2window_list)
    # 获取所有等候的票号，按时间排序
    ticket = BTicket.objects.filter(starttime__gte=today, state=0).order_by('starttime')
    print(ticket)
    if ticket is None:
        return redirect('BAdmin:ticket_list')
    tic_id = -1
    for tic in ticket:
        print('!!!!!!')
        print(tic.service)
        # 按照业务进行过滤，遇到第一个就退出循环，当下一个next
        for ser in service2window_list:
            if tic.service == ser.service:
                tic_id = tic.id
                break
        if tic_id != -1:
            break
    print(tic_id)
    try:
        ticket_next = BTicket.objects.get(id=tic_id)
    except:
        return redirect('BAdmin:ticket_list')

    ticket_next.state = 1
    # 让前台播放语音
    # print(ticket_next.no)
    # req.session["ticketno"] = ticket_next.no
    now = datetime.datetime.now()
    ticket_next.dotime = now
    ticket_next.user = window2user.user    # 将办理人和办理业务对应上
    ticket_next.window = window2user.window
    ticket_next.hold0 = '1'
    ticket_next.save()
    return redirect('BAdmin:ticket_list')


def call_back(req):
    username = req.session.get('username', None)
    if username is None:
        return redirect('BAdmin:blogin')
    buser = BUser.objects.get(username=username)

    try:
        ticket_call_back = BTicket.objects.filter(state=1, user=buser).first()
        print(ticket_call_back)
        ticket_call_back.hold0 = '1'
        ticket_call_back.save()
    except:
        pass
    return redirect('BAdmin:ticket_list')


# 票号办理
def ticket_doing(req, id):
    username = req.session.get('username', None)
    if username is None:
        return redirect('BAdmin:blogin')
    buser = user = BUser.objects.get(username=username)
    try:
        window2user = BUser2Window.objects.filter(user=buser).first()
    except:
        return redirect('BAdmin:window_2_user')

    ticket = BTicket.objects.get(id = id)
    ticket.state = 1
    ticket.user = window2user.user    # 将办理人和办理业务对应上
    ticket.user = window2user.window
    ticket.save()
    return redirect('BAdmin:ticket_list')




# 票号办结
def ticket_end(req, id):
    ticket = BTicket.objects.get(id = id)
    ticket.state = 2
    now = datetime.datetime.now()
    ticket.endtime = now
    ticket.save()
    return redirect('BAdmin:ticket_list')

# 作废
def ticket_out(req, id):
    ticket = BTicket.objects.get(id = id)
    ticket.state = 3
    now = datetime.datetime.now()
    ticket.outtime = now
    ticket.save()
    return redirect('BAdmin:ticket_list')

# 随机码的新增和显示
def random_list(req):
    username = req.session.get('username', None)
    if username is None:
        return redirect('BAdmin:blogin')

    if req.method == 'GET':
        randomlist = Brandonnumber.objects.all()
        return render(req, 'BAdmin/ticket_random_list.html', {'randomlist':randomlist})
    else:
        number = req.POST.get("met_randomnumber", None)
        if number:
            randomnumber = Brandonnumber.objects.create(number=number)
            return redirect('BAdmin:random_list')
        else:
            return redirect('BAdmin:random_list')



def window_list(req):
    if req.method == 'GET':
        windowlist = BWindow.objects.all()
        return render(req, 'BAdmin/window_list.html', {'windowlist':windowlist})
    else:
        window_name = req.POST.get('met_window_name', None)
        if window_name:
            try:
                window = BWindow.objects.create(name=window_name)
            except:
                return redirect('BAdmin:window_list')
            return redirect('BAdmin:window_list')
        return redirect('BAdmin:uwindow_list')


def window_delete(req, id):
    window = BWindow.objects.get(id = id)
    window.delete()
    return redirect('BAdmin:window_list')


def window_2_user(req):
    username = req.session.get('username', None)
    if username is None:
        return redirect('BAdmin:blogin')
    buser = user = BUser.objects.get(username=username)
    windowlist = BWindow.objects.all()
    if req.method == 'GET':
        try:
            window2user = BUser2Window.objects.filter(user=buser).first()
            state = True
            return render(req, 'BAdmin/window_2_user.html', {'windowlist': windowlist,
                                                             'state':state,
                                                             'window2user':window2user,
                                                             'buser':buser})
        except:
            state = False
            return render(req, 'BAdmin/window_2_user.html', {'windowlist':windowlist, 'state': state,'buser':buser})
    else:
        windowid = req.POST.get('met_windowid', None)
        if windowid:
            window = BWindow.objects.get(id = windowid)
            try:
                window2user = BUser2Window.objects.filter(user=buser).first()
                window2user.window = window
                window2user.save()
            except:
                window2user = BUser2Window.objects.create(user=buser, window = window)

            state = True
            return render(req, 'BAdmin/window_2_user.html', {'windowlist': windowlist,
                                                             'state':state,
                                                             'window2user':window2user,
                                                             'buser':buser})



def random_delete(req, id):
    random = Brandonnumber.objects.get(id = id).delete()
    return redirect('BAdmin:random_list')


def random_change(req, id):
    random = Brandonnumber.objects.get(id = id)
    if random.state:
        random.state = False
        random.save()
    else:
        random.state = True
        random.save()
    return redirect('BAdmin:random_list')


def user_data(req, id):
    username = req.session.get('username', None)
    if username is None:
        return redirect('BAdmin:blogin')

    buser = BUser.objects.get(id = id)

    if req.method == 'GET':
        return render(req, 'BAdmin/user_data.html', {'buser':buser})
    else:
        name = req.POST.get("met_name", None)
        phone = req.POST.get("met_phone", None)
        password = req.POST.get("met_password", None)
        if name and phone:
            buser.username = name
            buser.phone = phone
            buser.save()
        if password:
            buser.password = password
            buser.save()
        return render(req, 'BAdmin/user_data.html', {'buser': buser})


def user_list(req):
    if req.method == 'GET':
        buserlist = BUser.objects.exclude(name='admin').exclude(name='weber')
        return render(req, 'BAdmin/user_list.html', {'buserlist':buserlist})
    else:
        username = req.POST.get('met_name', None)
        password = req.POST.get('met_password', None)
        buser = BUser.objects.filter(username = username)
        if len(buser) > 0:
            return redirect('BAdmin:user_list')
        else:
            buser = BUser.objects.create(username=username, password=password, name=username)
            return redirect('BAdmin:user_list')


def user_delete(req, id):
    buser = BUser.objects.get(id = id).delete()
    return redirect('BAdmin:user_list')


def wechatuser_list(req):
    wechatuserlist = BWechatUser.objects.all()
    return render(req, 'BAdmin/wechatuser_list.html', {'wechatusetlist':wechatuserlist})


def wechatuser_delete(req, id):
    wechatuser = BWechatUser.objects.get(id = id).delete()
    return redirect('BAdmin:wechatuser_list')


def user_set(req, id):
    user = BUser.objects.get(id=id)
    if req.method == 'GET':
        return render(req, 'BAdmin/user_set.html', {'user':user})
    else:
        blog_power = int(req.POST.get('blog_power'))
        message_power = int(req.POST.get('message_power'))
        ticket_power = int(req.POST.get('ticket_power'))
        webword_power = int(req.POST.get('webword_power'))
        person_power = int(req.POST.get('person_power'))
        issuper = int(req.POST.get('issuper',0))

        user.blog = blog_power
        user.message = message_power
        user.ticket = ticket_power
        user.webword = webword_power
        user.person = person_power
        user.issuper = issuper
        if issuper == 1:
            user.blog = 2
            user.message = 2
            user.ticket = 2
            user.webword = 2
            user.person = 2
        user.save()

        return redirect('BAdmin:user_list')