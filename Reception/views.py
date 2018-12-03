from django.shortcuts import render, redirect
from BAdmin.models import *
from Blog.models import *
from WebWork.models import *
from Message.models import *
from django.http import HttpResponse
from CommunityService.wwAPI import *
from CommunityService.settings import *
from Ticket.models import *
from CommunityService.file_upload import *
import datetime


# Create your views here.


def login(req):
    # # 微信版
    # openid = req.session.get('openid', None)
    # wechatuser = BWechatUser.objects.get(openid=openid)
    # if openid is None:
    #     return redirect('Reception:communityshow')
    #
    # user = BWechatUser.objects.get(openid=openid)

    # 注册用户版
    name = req.session.get('name', None)
    if name is None:
        if req.method == 'GET':
            # return render(req, 'Reception/login.html', {})
            req.session['login_from'] = req.META.get('HTTP_REFERER', '/myindex')
            print(req.session['login_from'])
            return render(req, 'Reception/_login.html', {})
        else:
            # idcard = req.POST.get("met_idcard", None)
            password = req.POST.get("met_password", None)
            phone = req.POST.get("met_phone", None)

            wechatuserlist = BWechatUser.objects.filter(phone=phone, hold0=password)

            if len(wechatuserlist) == 0:
                title = "登陆失败"
                answer = "请输入正确的手机号码和密码。"
                return render(req, 'Reception/_loginanswer.html', {'title': title, 'answer': answer})
            else:
                wechatuser = wechatuserlist.first()
                idcard = wechatuser.idcard
                req.session["idcard"] = idcard
                return redirect(req.session['login_from'])
    else:

        return redirect('Reception:myindex')

def register(req):
    if req.method == 'GET':
        return render(req, 'Reception/_register.html',{})
    else:
        name = req.POST.get("met_name", None)
        idcard = req.POST.get("met_idcard", None)
        phone = req.POST.get("met_phone", None)

        wechatuserlist2 = BWechatUser.objects.filter(phone=phone)
        wechatuserlist3 = BWechatUser.objects.filter(idcard=idcard)

        if (len(wechatuserlist2) != 0) and (len(wechatuserlist3) != 0):
            title = "注册失败"
            answer = "该电话与证件已被注册"
            return render(req, 'Reception/_loginanswer.html', {'title': title, 'answer': answer})
        else:
            password1 = req.POST.get("met_password1", None)
            password2 = req.POST.get("met_password2", None)
            if password1 and password2 and (password1 == password2):
                wechatuser = BWechatUser.objects.create(name=name, idcard=idcard, phone=phone, hold0=password1)
                title = "注册成功"
                answer = "请回到登陆界面登陆。"
                return render(req, 'Reception/_loginanswer.html', {'title': title, 'answer': answer})
            else:
                title = "注册失败"
                answer = "请重新注册。"
                return render(req, 'Reception/_loginanswer.html', {'title': title, 'answer': answer})

def backpassword(req):
    if req.method == 'GET':
        return render(req, 'Reception/_backpassword.html', {})
    else:
        phone = req.POST.get("met_phone", None)
        idcard = req.POST.get("met_idcard", None)

        wechatuserlist = BWechatUser.objects.filter(phone=phone, idcard=idcard)

        if len(wechatuserlist) == 0:
            title = "重置失败"
            answer = "请输入正确的手机号码和对应证件号"
            return render(req, 'Reception/_loginanswer.html', {'title': title, 'answer': answer})
        else:
            password1 = req.POST.get("met_password1", None)
            password2 = req.POST.get("met_password2", None)
            if password1 and password2 and (password1==password2):
                wechatuser = wechatuserlist.first()
                wechatuser.hold0 = password1
                wechatuser.save()
                title = "重置成功"
                answer = "请回到登陆界面登陆"
                return render(req, 'Reception/_loginanswer.html', {'title': title, 'answer': answer})
            else:
                title = "重置失败"
                answer = "请输入正确的重置密码"
                return render(req, 'Reception/_loginanswer.html', {'title': title, 'answer': answer})

def communityshow(req):
    # # 微信服务号版
    # #wechatUrl = getCode(appid=APPID, redirect_url=REDIRECT_URI, scope=SCOPE, state=STATE)
    # wechatUrl = REDIRECT_URI  # 用于单机测试
    # code = req.GET.get('code', True)
    # state = req.GET.get('state', True)
    # if code and state:
    #     #temReqJson = getWebAccessToken(APPID, APPSECRET, code)
    #     temReqJson = {'openid':'sadninfsaiuhquir!#!$#!$@'} # 用于单机测试
    #     if temReqJson['openid']:
    #         communitydata = CommunityBase.objects.get(id=1)
    #         wuser = BWechatUser.objects.filter(openid=temReqJson['openid'])
    #         if len(wuser) == 0:
    #             wuser = BWechatUser.objects.create(openid=temReqJson['openid'])
    #         req.session['openid'] = temReqJson['openid']
    #         return render(req, 'Reception/communityshow.html', {'communitydata': communitydata})
    #     else:
    #         return redirect(wechatUrl)
    # else:
    #     return redirect(wechatUrl)
    # 用户注册版
    communitydata = CommunityBase.objects.get(id=1)
    return render(req, 'Reception/_index.html', {'communitydata': communitydata})

def contactus(req):
    contactdata = CommunityBase.objects.get(id = 2)
    return render(req, 'Reception/_contactus.html', {'contactdata':contactdata})

def showblog(req):
    bloglist = Article.objects.filter(state='发布')
    return render(req, 'Reception/_showblog.html', {'bloglist':bloglist})

def getblog(req, blogno):
    if req.method == 'GET':
        blog = Article.objects.get(id = blogno)
        return render(req, 'Reception/_getblog.html', {'blog':blog})

def showshixiangtype(req):
    shixiangtypelist = ShiXiangType.objects.all()
    return render(req, 'Reception/_showshixiangtype.html', locals())

def showshixiang(req, typeid):
    type = ShiXiangType.objects.get(id = typeid)
    shixianglist = ShiXiang.objects.filter(type=type, sxzt='发布')
    print(shixianglist)
    return render(req, 'Reception/_showshixiang.html', {'shixianglist':shixianglist, 'type':type})

def getshixiang(req, bh):
    if req.method == 'GET':
        shixiang = ShiXiang.objects.get(bh=bh)
        switch_file_list = []
        must_file_list = []
        if shixiang.switch0 == 1:
            temp = {"url":shixiang.file0, "name":shixiang.note0}
            switch_file_list.append(temp)
            if shixiang.must0 == 1:
                must_file_list.append(temp)
        if shixiang.switch1 == 1:
            temp = {"url": shixiang.file1, "name": shixiang.note1}
            switch_file_list.append(temp)
            if shixiang.must1 == 1:
                must_file_list.append(temp)
        if shixiang.switch2 == 1:
            temp = {"url":shixiang.file2, "name":shixiang.note2}
            switch_file_list.append(temp)
            if shixiang.must2 == 1:
                must_file_list.append(temp)
        if shixiang.switch3 == 1:
            temp = {"url":shixiang.file3, "name":shixiang.note3}
            switch_file_list.append(temp)
            if shixiang.must3 == 1:
                must_file_list.append(temp)
        if shixiang.switch4 == 1:
            temp = {"url":shixiang.file4, "name":shixiang.note4}
            switch_file_list.append(temp)
            if shixiang.must4 == 1:
                must_file_list.append(temp)
        if shixiang.switch5 == 1:
            temp = {"url":shixiang.file5, "name":shixiang.note5}
            switch_file_list.append(temp)
            if shixiang.must5 == 1:
                must_file_list.append(temp)
        if shixiang.switch6 == 1:
            temp = {"url":shixiang.file6, "name":shixiang.note6}
            switch_file_list.append(temp)
            if shixiang.must6 == 1:
                must_file_list.append(temp)
        if shixiang.switch7 == 1:
            temp = {"url":shixiang.file7, "name":shixiang.note7}
            switch_file_list.append(temp)
            if shixiang.must7 == 1:
                must_file_list.append(temp)
        if shixiang.switch8 == 1:
            temp = {"url":shixiang.file8, "name":shixiang.note8}
            switch_file_list.append(temp)
            if shixiang.must8 == 1:
                must_file_list.append(temp)
        if shixiang.switch9 == 1:
            temp = {"url":shixiang.file9, "name":shixiang.note9}
            switch_file_list.append(temp)
            if shixiang.must9 == 1:
                must_file_list.append(temp)
        return render(req, 'Reception/_getshixiang.html',
                      {'shixiang':shixiang,'switch_file_list':switch_file_list,"must_file_list":must_file_list})
    else:
        shixiang = ShiXiang.objects.get(bh=bh)
        switch_file_list = []
        must_file_list = []
        if shixiang.switch0 == 1:
            temp = {"url":shixiang.file0, "name":shixiang.note0}
            switch_file_list.append(temp)
            if shixiang.must0 == 1:
                must_file_list.append(temp)
        if shixiang.switch1 == 1:
            temp = {"url": shixiang.file1, "name": shixiang.note1}
            switch_file_list.append(temp)
            if shixiang.must1 == 1:
                must_file_list.append(temp)
        if shixiang.switch2 == 1:
            temp = {"url":shixiang.file2, "name":shixiang.note2}
            switch_file_list.append(temp)
            if shixiang.must2 == 1:
                must_file_list.append(temp)
        if shixiang.switch3 == 1:
            temp = {"url":shixiang.file3, "name":shixiang.note3}
            switch_file_list.append(temp)
            if shixiang.must3 == 1:
                must_file_list.append(temp)
        if shixiang.switch4 == 1:
            temp = {"url":shixiang.file4, "name":shixiang.note4}
            switch_file_list.append(temp)
            if shixiang.must4 == 1:
                must_file_list.append(temp)
        if shixiang.switch5 == 1:
            temp = {"url":shixiang.file5, "name":shixiang.note5}
            switch_file_list.append(temp)
            if shixiang.must5 == 1:
                must_file_list.append(temp)
        if shixiang.switch6 == 1:
            temp = {"url":shixiang.file6, "name":shixiang.note6}
            switch_file_list.append(temp)
            if shixiang.must6 == 1:
                must_file_list.append(temp)
        if shixiang.switch7 == 1:
            temp = {"url":shixiang.file7, "name":shixiang.note7}
            switch_file_list.append(temp)
            if shixiang.must7 == 1:
                must_file_list.append(temp)
        if shixiang.switch8 == 1:
            temp = {"url":shixiang.file8, "name":shixiang.note8}
            switch_file_list.append(temp)
            if shixiang.must8 == 1:
                must_file_list.append(temp)
        if shixiang.switch9 == 1:
            temp = {"url":shixiang.file9, "name":shixiang.note9}
            switch_file_list.append(temp)
            if shixiang.must9 == 1:
                must_file_list.append(temp)
        return render(req, 'Reception/_getshixiang.html',
                      {'shixiang':shixiang,'switch_file_list':switch_file_list,"must_file_list":must_file_list})

def setshixiang(req, bh):
    # # 微信版
    # openid = req.session.get('openid', None)
    # wechatuser = BWechatUser.objects.get(openid=openid)
    # if openid is None:
    #     return redirect('Reception:communityshow')
    #
    # user = BWechatUser.objects.get(openid=openid)

    # 注册用户版
    idcard = req.session.get('idcard')

    if idcard is None:
        return redirect('Reception:login')

    wechatuser = BWechatUser.objects.filter(idcard=idcard).first()

    if wechatuser.hold1 == '1':
        return render(req, 'Reception/_need_register.html', {})

    shixiang = ShiXiang.objects.get(bh = bh)

    if req.method == 'GET':
        print('in get')
        switch_file_list = []
        must_file_list = []
        if shixiang.switch0 == 1:
            temp = {"url": shixiang.file0, "name": shixiang.note0}
            switch_file_list.append(temp)
            if shixiang.must0 == 1:
                must_file_list.append(temp)
        if shixiang.switch1 == 1:
            temp = {"url": shixiang.file1, "name": shixiang.note1}
            switch_file_list.append(temp)
            if shixiang.must1 == 1:
                must_file_list.append(temp)
        if shixiang.switch2 == 1:
            temp = {"url": shixiang.file2, "name": shixiang.note2}
            switch_file_list.append(temp)
            if shixiang.must2 == 1:
                must_file_list.append(temp)
        if shixiang.switch3 == 1:
            temp = {"url": shixiang.file3, "name": shixiang.note3}
            switch_file_list.append(temp)
            if shixiang.must3 == 1:
                must_file_list.append(temp)
        if shixiang.switch4 == 1:
            temp = {"url": shixiang.file4, "name": shixiang.note4}
            switch_file_list.append(temp)
            if shixiang.must4 == 1:
                must_file_list.append(temp)
        if shixiang.switch5 == 1:
            temp = {"url": shixiang.file5, "name": shixiang.note5}
            switch_file_list.append(temp)
            if shixiang.must5 == 1:
                must_file_list.append(temp)
        if shixiang.switch6 == 1:
            temp = {"url": shixiang.file6, "name": shixiang.note6}
            switch_file_list.append(temp)
            if shixiang.must6 == 1:
                must_file_list.append(temp)
        if shixiang.switch7 == 1:
            temp = {"url": shixiang.file7, "name": shixiang.note7}
            switch_file_list.append(temp)
            if shixiang.must7 == 1:
                must_file_list.append(temp)
        if shixiang.switch8 == 1:
            temp = {"url": shixiang.file8, "name": shixiang.note8}
            switch_file_list.append(temp)
            if shixiang.must8 == 1:
                must_file_list.append(temp)
        if shixiang.switch9 == 1:
            temp = {"url": shixiang.file9, "name": shixiang.note9}
            switch_file_list.append(temp)
            if shixiang.must9 == 1:
                must_file_list.append(temp)
        return render(req, 'Reception/_setshixiang.html',
                      {'wechatuser':wechatuser, 'shixiang':shixiang,'switch_file_list':switch_file_list,'must_file_list':must_file_list})
    else:
        print("in post")
        senddata = req.POST.get("met_sendcontent", "无")
        print(senddata)
        if senddata:
            file_list = req.FILES.getlist('file')
            file_name_list = req.POST.getlist('filename')
            toshixiang = toShiXiang.objects.create(shixiang=shixiang,
                                                   wechatuser=wechatuser,
                                                   senddata=senddata,
                                                   backcontent="",
                                                   state='待分派',
                                                   rank='待评价')
            print(len(file_list))
            for filename in file_name_list:
                if toshixiang.file0 == '':
                    toshixiang.note0 = str(filename).replace('上传','')
                    toshixiang.save()
                elif toshixiang.file1 == '':
                    toshixiang.note1 = str(filename).replace('上传', '')
                    toshixiang.save()
                elif toshixiang.file2 == '':
                    toshixiang.note2 = str(filename).replace('上传', '')
                    toshixiang.save()
                elif toshixiang.file3 == '':
                    toshixiang.note3 = str(filename).replace('上传', '')
                    toshixiang.save()
                elif toshixiang.file4 == '':
                    toshixiang.note4 = str(filename).replace('上传', '')
                    toshixiang.save()
                elif toshixiang.file5 == '':
                    toshixiang.note5 = str(filename).replace('上传', '')
                    toshixiang.save()
                elif toshixiang.file6 == '':
                    toshixiang.note6 = str(filename).replace('上传', '')
                    toshixiang.save()
                elif toshixiang.file7 == '':
                    toshixiang.note7 = str(filename).replace('上传', '')
                    toshixiang.save()
                elif toshixiang.file8 == '':
                    toshixiang.note8 = str(filename).replace('上传', '')
                    toshixiang.save()
                elif toshixiang.file9 == '':
                    toshixiang.note9 = str(filename).replace('上传', '')
                    toshixiang.save()
            for file in file_list:
                upload_answer = file_upload(file, 'Reception')
                if toshixiang.file0 == '':
                    toshixiang.file0 = upload_answer["url"]
                    toshixiang.save()
                elif toshixiang.file1 == '':
                    toshixiang.file1 = upload_answer["url"]
                    toshixiang.save()
                elif toshixiang.file2 == '':
                    toshixiang.file2 = upload_answer["url"]
                    toshixiang.save()
                elif toshixiang.file3 == '':
                    toshixiang.file3 = upload_answer["url"]
                    toshixiang.save()
                elif toshixiang.file4 == '':
                    toshixiang.file4 = upload_answer["url"]
                    toshixiang.save()
                elif toshixiang.file5 == '':
                    toshixiang.file5 = upload_answer["url"]
                    toshixiang.save()
                elif toshixiang.file6 == '':
                    toshixiang.file6 = upload_answer["url"]
                    toshixiang.save()
                elif toshixiang.file7 == '':
                    toshixiang.file7 = upload_answer["url"]
                    toshixiang.save()
                elif toshixiang.file8 == '':
                    toshixiang.file8 = upload_answer["url"]
                    toshixiang.save()
                elif toshixiang.file9 == '':
                    toshixiang.file9 = upload_answer["url"]
                    toshixiang.save()
                toshixiang.save()
            return render(req, 'Reception/_setshixiangsuccess.html', None)
        else:
            return render(req, 'Reception/_setshixiang.html', {'wechatuser':wechatuser, 'shixiang':shixiang})

def setmessage(req):
    # # 微信版
    # openid = req.session.get('openid', None)
    # wechatuser = BWechatUser.objects.get(openid=openid)
    # if openid is None:
    #     return redirect('Reception:communityshow')
    #
    # user = BWechatUser.objects.get(openid=openid)

    # 注册用户版
    idcard = req.session.get('idcard')

    if idcard is None:
        return redirect('Reception:login')

    wechatuser = BWechatUser.objects.filter(idcard=idcard).first()
    if wechatuser.hold1 == '1':
        return render(req, 'Reception/_need_register.html',{})

    if req.method == 'GET':
        return render(req, 'Reception/_setmessage.html', {'wechatuser':wechatuser})
    else:
        sendname = req.POST.get("met_sendname", None)
        sendphone = req.POST.get('met_sendphone', None)
        sendtitle = req.POST.get('met_sendtitle','无')
        sendcontent = req.POST.get('met_sendcontent', None)
        file_list = req.FILES.getlist('file')
        print(sendname, sendphone, sendtitle, sendcontent)
        if sendname and sendphone and sendcontent:
            message = Message.objects.create(sendname=sendname,
                                             sendtitle=sendtitle,
                                             sendphone=sendphone,
                                             sendcontent = sendcontent,
                                             backname='待回复',
                                             backcontent='待回复',
                                             wechat = wechatuser,
                                             process='待分派')
            print('save message')
            print(message.file0)
            try:
                print(len(file_list))
                for file in file_list:
                    upload_answer = file_upload(file, 'Message')
                    if message.file0 == '':

                        message.file0 = upload_answer["url"]
                        message.save()
                    elif message.file1 == '':
                        message.file1 = upload_answer["url"]
                        message.save()
                    elif message.file2 == '':
                        message.file2 = upload_answer["url"]
                        message.save()
            except:
                pass
            return render(req, 'Reception/_setmessagesuccess.html', {})
        else:
            return render(req, 'Reception/_setmessage.html', {'wechatuser':wechatuser})

def showmessage(req):
    messagelist = Message.objects.filter(state='公开')
    return render(req, 'Reception/_showmessage.html', locals())

def getmessage(req, id):
    message = Message.objects.get(id = id)
    return render(req, 'Reception/_getmessage.html', locals())

def ticket_wait(req):
    # 构造一个序列: 业务名称;等候人数;当前办理票号;下一个票号
    today = datetime.date.today()
    servicelist = BService.objects.all()
    windowlist = BWindow.objects.all()
    ticketlist = BTicket.objects.filter(starttime__gte=today).order_by('starttime')
    waitlist = []
    # for service in servicelist:
    #     wait = {}
    #     count = len(ticketlist.filter(service=service, state=0))
    #
    #     doing = ticketlist.filter(service=service, state=1).first()
    #
    #     next = ticketlist.filter(service=service, state=0).first()
    #
    #     wait["service"] = service
    #
    #     wait["count"] = count
    #
    #     wait["doing"] = doing
    #
    #     wait["net"] = next
    #
    #     waitlist.append(wait)
    # 修改为以窗口为主体
    # 构造序列{窗口；等候人数；当前办理；下一个办理}
    for window in windowlist:
        wait = {}
        count = 0
        service2window_list = BWindow2Service.objects.filter(window=window)
        temp_queueset = ticketlist.filter(id = -1) # 构造一个空序列
        for service2window in service2window_list:
            service_count_list = ticketlist.filter(service=service2window.service) # 获取该业务的票号序列
            temp_count = len(service_count_list.filter(state=0)) # 计算该业务等候人数
            count = count + temp_count # 计算该窗口等候人数
            # 构造该窗口下所有业务的序列,可以从这个直接
            # 计算出正在办理，等候人数，下一个号
            temp_queueset = temp_queueset | service_count_list

        doing = temp_queueset.filter(state=1).order_by('dotime')
        next = temp_queueset.filter(state=0).order_by('starttime').first()
        wait["window"] = window
        wait["count"] = count
        wait["doing"] = doing
        wait["net"] = next
        waitlist.append(wait)
    return render(req, 'Reception/_ticket_wait.html', {'waitlist':waitlist, 'today':today})

def ticket_show(req):
    # 构造一个序列: 业务名称;等候人数;当前办理票号;下一个票号

    # 可以通过前台获取票号，给播放语音的票号一个标志
    try:
        ticket_call_end_id = req.GET.get("ticketno", None)
        if ticket_call_end_id:
            ticket_call_end = BTicket.objects.get(id = ticket_call_end_id)
            ticket_call_end.hold0 = '0'
            ticket_call_end.save()
    except:
        pass

    today = datetime.date.today()
    servicelist = BService.objects.all()
    windowlist = BWindow.objects.all()
    ticketlist = BTicket.objects.filter(starttime__gte=today).order_by('starttime')
    temp_session_ticket = req.session.get("ticketno",None)
    waitlist = []
    # for service in servicelist:
    #     wait = {}
    #     count = len(ticketlist.filter(service=service, state=0))
    #
    #     doing = ticketlist.filter(service=service, state=1).first()
    #
    #     next = ticketlist.filter(service=service, state=0).first()
    #
    #     wait["service"] = service
    #
    #     wait["count"] = count
    #
    #     wait["doing"] = doing
    #
    #     wait["net"] = next
    #
    #     waitlist.append(wait)
    # 修改为以窗口为主体
    # 构造序列{窗口；等候人数；当前办理；下一个办理}
    for window in windowlist:
        wait = {}
        count = 0
        service2window_list = BWindow2Service.objects.filter(window=window)
        temp_queueset = ticketlist.filter(id = -1) # 构造一个空序列
        for service2window in service2window_list:
            service_count_list = ticketlist.filter(service=service2window.service) # 获取该业务的票号序列
            temp_count = len(service_count_list.filter(state=0)) # 计算该业务等候人数
            count = count + temp_count # 计算该窗口等候人数
            # 构造该窗口下所有业务的序列,可以从这个直接
            # 计算出正在办理，等候人数，下一个号
            temp_queueset = temp_queueset | service_count_list

        doing = temp_queueset.filter(state=1).order_by('dotime')
        next = temp_queueset.filter(state=0).order_by('starttime').first()
        wait["window"] = window
        wait["count"] = count
        wait["doing"] = doing
        wait["net"] = next
        waitlist.append(wait)

        try:
            ticket_call_start = BTicket.objects.filter(hold0='1').order_by('dotime').first()
            if ticket_call_start:
                call_state = True

            else:
                ticket_call_start = None
                call_state = False
        except:
            ticket_call_start = None
            call_state = False

    return render(req, 'Reception/_ticket_show.html', {'waitlist':waitlist, 'today':today,
                                                       'ticket_call_start':ticket_call_start,
                                                       'call_state':call_state})

def ticket_get(req):
    # # 微信版
    # openid = req.session.get('openid', None)
    # wechatuser = BWechatUser.objects.get(openid=openid)
    # if openid is None:
    #     return redirect('Reception:communityshow')
    #
    # user = BWechatUser.objects.get(openid=openid)


    # 注册用户版
    idcard = req.session.get('idcard')

    if idcard is None:
        return redirect('Reception:login')
    try:
        wechatuser = BWechatUser.objects.filter(idcard=idcard).first()
    except:
        req.session["idcard"] = None
        return redirect('Reception:random_check')

    servicelist = BService.objects.filter(state='支持')
    if req.method == 'GET':
        print(servicelist)
        return render(req, 'Reception/_ticket_get.html', {'wechatuser':wechatuser, 'servicelist':servicelist})
    else:
        serviceid = req.POST.get('met_serviceid', None)
        # 限号
        wechatuserticketlist = BTicket.objects.filter(starttime__gte=datetime.date.today(), wechatuser=wechatuser, state='0')
        if len(wechatuserticketlist) > 1:
            title = "取号失败"
            answer = "您已达到每天取号的上限."
            return render(req, 'Reception/_ticket_get_answer.html', {'title':title, 'answer':answer})

        if serviceid:
            today = datetime.date.today()
            service = BService.objects.get(id=serviceid)
            ticketno = BTicket.objects.filter(service=service, starttime__gte=today)
            ticketno = len(ticketno) + 1
            ticketno = service.type + str(ticketno)
            print(ticketno)
            ticket = BTicket.objects.create(
                service = service,
                wechatuser = wechatuser,
                no=ticketno,
                type=False, # false代表现场取号,
                state=0,
                starttime=datetime.datetime.now()
            )
            print(ticket)
            title = '取票成功'
            answer = '取票成功, 票号为:'+ ticket.no + '。<br>窗口号:'+ service.window +'' \
                                                                            '。<br>备注：1、请留意呼号情况，过号须从新取号。' \
                                                                            '<br>2、如是匿名取号，请及时注册账号以便日后使用。' \
                                                                            '<br>3、请关注长富社区公众号，以获取最新咨询。'
            return render(req, 'Reception/_ticket_get_answer.html', {'title':title, 'answer':answer})

def ticket_get_pc(req):
    servicelist = BService.objects.filter(state='支持')
    printTicket = {"state":0}
    if req.method == 'GET':
        print(servicelist)
        return render(req, 'Reception/_ticket_get_pc.html', {'servicelist':servicelist,'printTicket':printTicket})
    else:
        serviceid = req.POST.get('met_serviceid', None)
        try:
            wechatuser_temp = BWechatUser.objects.get(id = 9999)
        except:
            wechatuser_temp = BWechatUser.objects.create(id = 9999,
                                                         name='临时用户',
                                                         idcard='123456789012345678',
                                                         phone='77777777777',
                                                         hold0='!@#$%^&*()')
        if serviceid:
            today = datetime.date.today()
            service = BService.objects.get(id=serviceid)
            ticketno = BTicket.objects.filter(service=service, starttime__gte=today)
            ticketno = len(ticketno) + 1
            ticketno = service.type + str(ticketno)
            print(ticketno)
            ticket = BTicket.objects.create(
                service = service,
                wechatuser = wechatuser_temp,
                no=ticketno,
                type=False, # false代表现场取号,
                state=0,
                starttime=datetime.datetime.now()
            )
            printTicket["state"] = 1
            printTicket["url"] = "http://changfushequ.top/Reception/ticket_assess/?ticketid=" + str(ticket.id)
            # printTicket["url"] = "http://127.0.0.1:8000/Reception/ticket_assess/?ticketid=" + str(ticket.id)
            return render(req, 'Reception/_ticket_get_pc.html',
                          {'servicelist': servicelist, 'printTicket': printTicket, 'ticket':ticket})
        return render(req, 'Reception/_ticket_get_pc.html', {'servicelist': servicelist, 'printTicket': printTicket})

def service_show_pc(req):
    pass

def ticket_appoint(req):
    # # 微信版
    # openid = req.session.get('openid', None)
    # wechatuser = BWechatUser.objects.get(openid=openid)
    # if openid is None:
    #     return redirect('Reception:communityshow')
    #
    # user = BWechatUser.objects.get(openid=openid)

    # 注册用户版
    idcard = req.session.get('idcard')

    if idcard is None:
        return redirect('Reception:login')

    wechatuser = BWechatUser.objects.filter(idcard=idcard).first()
    today = datetime.datetime.today()
    if req.method == 'GET':
        servicelist = BService.objects.filter(state='支持')
        datelist = []
        for i in range(1, 4):
            date = {}
            temp = today + datetime.timedelta(days=i)
            date["year"] = temp.year
            date["month"] = temp.month
            date["day"] = temp.day
            datelist.append(date)
        return render(req, 'Reception/ticket_appoint.html', {'datelist': datelist, 'servicelist': servicelist})
    else:
        # 限号
        wechatuserticketlist = BTicket.objects.filter(starttime__gte=datetime.date.today(), wechatuser=wechatuser, state='4')
        if len(wechatuserticketlist) > 2:
            title = "预约失败"
            answer = "您已达到预约取号的上限."
            return render(req, 'Reception/_ticket_get_answer.html', {'title':title, 'answer':answer})
        serviceid = req.POST.get('met_serviceid', None)
        day = req.POST.get('met_day', None)
        hour = req.POST.get('met_hour', None)
        datestr = day + ' ' + hour + ':00:00'
        starttime = datetime.datetime.strptime(datestr, "%Y-%m-%d %H:%M:%S")
        if serviceid:
            service = BService.objects.get(id=serviceid)
            ticketno = BTicket.objects.filter(service=service, starttime__gte=today)
            ticketno = len(ticketno) + 1
            ticketno = service.type + str(ticketno)
            print(ticketno)
            ticket = BTicket.objects.create(
                service = service,
                wechatuser = wechatuser,
                no=ticketno,
                type=True, # false代表现场取号,
                state="4",
                starttime=starttime,
                queuetime=datetime.datetime.now()
            )
            print(ticket)
            title = '预约成功'
            answer = '预约成功,请在预约时间段内到达现场确认预约。'
            return render(req, 'Reception/_ticket_get_answer.html', {'title':title, 'answer':answer})

def random_check(req):
    # # 微信版
    # openid = req.session.get('openid', None)
    # wechatuser = BWechatUser.objects.get(openid=openid)
    # if openid is None:
    #     return redirect('Reception:communityshow')
    #
    # user = BWechatUser.objects.get(openid=openid)

    # 注册用户版
    idcard = req.session.get('idcard')

    now = req.GET.get('now', None)
    # print(now)
    # print(type(now))
    if (idcard is None) and (now != '1'):
        return redirect('Reception:login')


    # # 将之前临时的账号修改为一个临时用户
    # today = datetime.date.today()
    # wechatuser_list_g = BWechatUser.objects.filter(addtime__lte=today, hold1='1')
    # try:
    #     wechatuser_temp = BWechatUser.objects.get(id = 9999)
    # except:
    #     wechatuser_temp = BWechatUser.objects.create(id = 9999,
    #                                                  name='临时用户',
    #                                                  idcard='123456789012345678',
    #                                                  phone='77777777777',
    #                                                  hold0='!@#$%^&*()')
    # for wechatuser in wechatuser_list_g:
    #     wechatuser_ticket_list = BTicket.objects.filter(wechatuser=wechatuser)
    #     for ticket_temp in wechatuser_ticket_list:
    #         ticket_temp.wechatuser = wechatuser_temp
    #     wechatuser.delete()



    # 这里做匿名取号
    # Reception/random_check/?now=1
    if (idcard is None) and (now == '1'):
        now = str(datetime.datetime.now().time())[0:10]
        temp = 'g'+now
        print(temp)
        wechatuser = BWechatUser.objects.create(name=temp ,idcard=temp, phone=temp, hold0=1, hold1='1')
        req.session["idcard"] = wechatuser.idcard
        return redirect('Reception:random_check')
    print(idcard)

    # check user

    if req.method =='GET':
        return render(req, 'Reception/_random_check.html', {})
    else:
        number = req.POST.get('met_randomnumber', None)
        if number:
            numberlist = Brandonnumber.objects.filter(number=number)
            if len(numberlist) > 0:
                return redirect('Reception:ticket_get')
            else:
                title = '验证失败'
                answer = '请输入正确的验证码'
                return render(req, 'Reception/_ticket_get_answer.html', {'title':title, 'answer':answer})
        else:
            return render(req, 'Reception/_random_check.html', {})

def bticket_assess(req):
    ticket_id = req.GET.get('ticketid', None)
    try:
        ticket = BTicket.objects.get(id=ticket_id)
        print(ticket)
    except:
        pass
    if req.method == 'GET':
        return render(req, 'Reception/_ticketassess.html', {'ticket': ticket})
    else:
        assess_level = req.POST.get('assess_level', None)
        assess_content = req.POST.get('assess_content', '')
        assess = BAssess.objects.create(level=int(assess_level), content=assess_content)
        ticket.assess = assess
        ticket.save()
        return render(req, 'Reception/_setassesssuccess.html', {})

def need_register(req):
    return render(req, 'Reception/_need_register.html',{})

def wechaturlpower(req):
    return HttpResponse('asdndsafniaofds')

def myindex(req):
    # # 微信版专用
    # openid = req.session.get('openid', None)
    # if openid:
    #     return render(req, 'Reception/myindex.html',{})
    # else:
    #     return redirect('Reception:login')

    # 注册用户用
    idcard = req.session.get('idcard', None)
    if idcard:
        lastblog = Article.objects.first()
        return render(req, 'Reception/_myindex.html', {'lastblog':lastblog})
    else:
        return redirect('Reception:login')

def mymessage(req):
    # # 微信版
    # openid = req.session.get('openid', None)
    # wechatuser = BWechatUser.objects.get(openid=openid)
    # if openid is None:
    #     return redirect('Reception:communityshow')
    #
    # user = BWechatUser.objects.get(openid=openid)

    # 注册用户版
    idcard = req.session.get('idcard')

    if idcard is None:
        return redirect('Reception:login')

    wechatuser = BWechatUser.objects.get(idcard=idcard)

    messagelist = Message.objects.filter(wechat=wechatuser).exclude(state='隐藏')
    print(messagelist)

    return render(req, 'Reception/_mymessage.html', {'messagelist':messagelist})

def myshixiang(req):
    # # 微信版
    # openid = req.session.get('openid', None)
    # wechatuser = BWechatUser.objects.get(openid=openid)
    # if openid is None:
    #     return redirect('Reception:communityshow')
    #
    # user = BWechatUser.objects.get(openid=openid)

    # 注册用户版
    idcard = req.session.get('idcard')

    if idcard is None:
        return redirect('Reception:login')

    wechatuser = BWechatUser.objects.get(idcard=idcard)
    toshixianglist = toShiXiang.objects.filter(wechatuser=wechatuser).order_by('-addtime')
    return render(req, 'Reception/_myshixiang.html', {'toshixianglist':toshixianglist})

def mytoshixiang(req, id):
    # # 微信版
    # openid = req.session.get('openid', None)
    # wechatuser = BWechatUser.objects.get(openid=openid)
    # if openid is None:
    #     return redirect('Reception:communityshow')
    #
    # user = BWechatUser.objects.get(openid=openid)

    # 注册用户版
    idcard = req.session.get('idcard')

    if idcard is None:
        return redirect('Reception:login')

    wechatuser = BWechatUser.objects.get(idcard=idcard)
    toshixiang = toShiXiang.objects.get(id = id)
    file_list = []
    if toshixiang.file0:
        temp = {'name': toshixiang.note0, 'url': toshixiang.file0}
        file_list.append(temp)
    if toshixiang.file1:
        temp = {'name': toshixiang.note0, 'url': toshixiang.file1}
        file_list.append(temp)
    if toshixiang.file2:
        temp = {'name': toshixiang.note0, 'url': toshixiang.file2}
        file_list.append(temp)
    if toshixiang.file3:
        temp = {'name': toshixiang.note0, 'url': toshixiang.file3}
        file_list.append(temp)
    if toshixiang.file4:
        temp = {'name': toshixiang.note0, 'url': toshixiang.file4}
        file_list.append(temp)
    if toshixiang.file5:
        temp = {'name': toshixiang.note0, 'url': toshixiang.file5}
        file_list.append(temp)
    if toshixiang.file6:
        temp = {'name': toshixiang.note0, 'url': toshixiang.file6}
        file_list.append(temp)
    if toshixiang.file7:
        temp = {'name': toshixiang.note0, 'url': toshixiang.file7}
        file_list.append(temp)
    if toshixiang.file8:
        temp = {'name': toshixiang.note0, 'url': toshixiang.file8}
        file_list.append(temp)
    if toshixiang.file9:
        temp = {'name': toshixiang.note0, 'url': toshixiang.file9}
        file_list.append(temp)

    if req.method=="GET":
        if toshixiang.state == '退回':
            shixiang = toshixiang.shixiang
            switch_file_list = []
            must_file_list = []
            if shixiang.switch0 == 1:
                temp = {"url": shixiang.file0, "name": shixiang.note0}
                switch_file_list.append(temp)
                if shixiang.must0 == 1:
                    must_file_list.append(temp)
            if shixiang.switch1 == 1:
                temp = {"url": shixiang.file1, "name": shixiang.note1}
                switch_file_list.append(temp)
                if shixiang.must1 == 1:
                    must_file_list.append(temp)
            if shixiang.switch2 == 1:
                temp = {"url": shixiang.file2, "name": shixiang.note2}
                switch_file_list.append(temp)
                if shixiang.must2 == 1:
                    must_file_list.append(temp)
            if shixiang.switch3 == 1:
                temp = {"url": shixiang.file3, "name": shixiang.note3}
                switch_file_list.append(temp)
                if shixiang.must3 == 1:
                    must_file_list.append(temp)
            if shixiang.switch4 == 1:
                temp = {"url": shixiang.file4, "name": shixiang.note4}
                switch_file_list.append(temp)
                if shixiang.must4 == 1:
                    must_file_list.append(temp)
            if shixiang.switch5 == 1:
                temp = {"url": shixiang.file5, "name": shixiang.note5}
                switch_file_list.append(temp)
                if shixiang.must5 == 1:
                    must_file_list.append(temp)
            if shixiang.switch6 == 1:
                temp = {"url": shixiang.file6, "name": shixiang.note6}
                switch_file_list.append(temp)
                if shixiang.must6 == 1:
                    must_file_list.append(temp)
            if shixiang.switch7 == 1:
                temp = {"url": shixiang.file7, "name": shixiang.note7}
                switch_file_list.append(temp)
                if shixiang.must7 == 1:
                    must_file_list.append(temp)
            if shixiang.switch8 == 1:
                temp = {"url": shixiang.file8, "name": shixiang.note8}
                switch_file_list.append(temp)
                if shixiang.must8 == 1:
                    must_file_list.append(temp)
            if shixiang.switch9 == 1:
                temp = {"url": shixiang.file9, "name": shixiang.note9}
                switch_file_list.append(temp)
                if shixiang.must9 == 1:
                    must_file_list.append(temp)
        else:
            switch_file_list = []
            must_file_list = []
        return render(req,
                      'Reception/_mytoshixiang.html',
                      {'wechatuser':wechatuser, 'toshixiang':toshixiang,'file_list':file_list,
                       'switch_file_list':switch_file_list,'must_file_list': must_file_list,
                       })
    else:
        file_list = req.FILES.getlist('file')
        file_name_list = req.POST.getlist('filename')

        toshixiang.backcontent = ''
        toshixiang.state = '待分派'
        toshixiang.user = None
        toshixiang.file0 = ''
        toshixiang.file1 = ''
        toshixiang.file2 = ''
        toshixiang.file3 = ''
        toshixiang.file4 = ''
        toshixiang.file5 = ''
        toshixiang.file6 = ''
        toshixiang.file7 = ''
        toshixiang.file8 = ''
        toshixiang.file9 = ''
        toshixiang.note0 = None
        toshixiang.note1 = None
        toshixiang.note2 = None
        toshixiang.note3 = None
        toshixiang.note4 = None
        toshixiang.note5 = None
        toshixiang.note6 = None
        toshixiang.note7 = None
        toshixiang.note8 = None
        toshixiang.note9 = None

        toshixiang.save()
        print(len(file_list))
        for filename in file_name_list:
            if toshixiang.file0 == '':
                toshixiang.note0 = str(filename).replace('上传', '')
                toshixiang.save()
            elif toshixiang.file1 == '':
                toshixiang.note1 = str(filename).replace('上传', '')
                toshixiang.save()
            elif toshixiang.file2 == '':
                toshixiang.note2 = str(filename).replace('上传', '')
                toshixiang.save()
            elif toshixiang.file3 == '':
                toshixiang.note3 = str(filename).replace('上传', '')
                toshixiang.save()
            elif toshixiang.file4 == '':
                toshixiang.note4 = str(filename).replace('上传', '')
                toshixiang.save()
            elif toshixiang.file5 == '':
                toshixiang.note5 = str(filename).replace('上传', '')
                toshixiang.save()
            elif toshixiang.file6 == '':
                toshixiang.note6 = str(filename).replace('上传', '')
                toshixiang.save()
            elif toshixiang.file7 == '':
                toshixiang.note7 = str(filename).replace('上传', '')
                toshixiang.save()
            elif toshixiang.file8 == '':
                toshixiang.note8 = str(filename).replace('上传', '')
                toshixiang.save()
            elif toshixiang.file9 == '':
                toshixiang.note9 = str(filename).replace('上传', '')
                toshixiang.save()
        for file in file_list:
            upload_answer = file_upload(file, 'Reception')
            if toshixiang.file0 == '':
                toshixiang.file0 = upload_answer["url"]
                toshixiang.save()
            elif toshixiang.file1 == '':
                toshixiang.file1 = upload_answer["url"]
                toshixiang.save()
            elif toshixiang.file2 == '':
                toshixiang.file2 = upload_answer["url"]
                toshixiang.save()
            elif toshixiang.file3 == '':
                toshixiang.file3 = upload_answer["url"]
                toshixiang.save()
            elif toshixiang.file4 == '':
                toshixiang.file4 = upload_answer["url"]
                toshixiang.save()
            elif toshixiang.file5 == '':
                toshixiang.file5 = upload_answer["url"]
                toshixiang.save()
            elif toshixiang.file6 == '':
                toshixiang.file6 = upload_answer["url"]
                toshixiang.save()
            elif toshixiang.file7 == '':
                toshixiang.file7 = upload_answer["url"]
                toshixiang.save()
            elif toshixiang.file8 == '':
                toshixiang.file8 = upload_answer["url"]
                toshixiang.save()
            elif toshixiang.file9 == '':
                toshixiang.file9 = upload_answer["url"]
                toshixiang.save()
            toshixiang.save()
        return render(req, 'Reception/_setshixiangsuccess.html',{})

def mytoshixiang_assess(req, id):
    toshixiang = toShiXiang.objects.get(id = id)
    if req.method == 'GET':
        return render(req, 'Reception/_mytoshixiang_assess.html', {'toshixiang':toshixiang})
    else:
        rank = req.POST.get('met_rank',None)
        comment = req.POST.get('met_comment', '无')
        if rank:
            toshixiang.rank = rank
            toshixiang.comment = comment
            toshixiang.save()
            return render(req, 'Reception/_setassesssuccess.html', {})
        return render(req, 'Reception/_mytoshixiang_assess.html', {'toshixiang':toshixiang})

def mydata(req):
    # # 微信版
    # openid = req.session.get('openid', None)
    # wechatuser = BWechatUser.objects.get(openid=openid)
    # if openid is None:
    #     return redirect('Reception:communityshow')
    #
    # user = BWechatUser.objects.get(openid=openid)

    # 注册用户版
    idcard = req.session.get('idcard')

    if idcard is None:
        return redirect('Reception:login')

    wechatuser = BWechatUser.objects.filter(idcard=idcard).first()
    if req.method == 'GET':
        return render(req, 'Reception/_mydata.html', {'wechatuser': wechatuser})
    else:
        #phone = req.POST.get("met_phone", None)
        name = req.POST.get("met_name", None)
        if name:
            wechatuser.name = name
            wechatuser.hold1 = ''
            wechatuser.save()
            return redirect('Reception:myindex')
        else:
            return redirect('Reception:mydata')

def myticket(req):

    # # 微信版
    # openid = req.session.get('openid', None)
    # wechatuser = BWechatUser.objects.get(openid=openid)
    # if openid is None:
    #     return redirect('Reception:communityshow')
    #
    # user = BWechatUser.objects.get(openid=openid)

    # 注册用户版
    idcard = req.session.get('idcard')

    if idcard is None:
        return redirect('Reception:login')

    today = datetime.date.today()
    wechatuser = BWechatUser.objects.filter(idcard=idcard).first()
    myticketlist = BTicket.objects.filter(wechatuser=wechatuser, starttime__gte=today)
    return render(req, 'Reception/_myticket.html', {'myticketlist': myticketlist})