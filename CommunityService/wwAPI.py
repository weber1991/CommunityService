import requests
import json
import urllib.parse

'''
weber wechat API
date:2018-03-26
version:1.0
'''


'''
微信网页授权四个步骤：
1、获取code
2、code换取access_token
3、刷新access_token（非必要）
4、获取用户信息（若scope为snsapi_userinfo）
'''


def getCode(appid=None, redirect_url=None, state='wwAPI', scope='snsapi_base'):
    '''
    引导用户打开wechatUrl以获取code
    :param appid:
    :param redirect_url:need urlencode
    :param scope:(default)snsapi_base, snsapi_userinfo
    :param state:用户自定义可带
    :return:
    '''
    wechatUrl = "https://open.weixin.qq.com/connect/oauth2/authorize?" \
                "appid=APPID&redirect_uri=REDIRECT_URI&response_type=code&scope=snsapi_base&state=STATE#wechat_redirect"
    if appid is None:
        return "need appid"
    if redirect_url is None:
        return "need redirect_url"
    if ((scope!="snsapi_base") and (scope!="snsapi_userinfo")):
        return "scope not right"
    elif (scope == "snsapi_userinfor"):
        wechatUrl = wechatUrl.replace("SCOPE", scope)

    wechatUrl = wechatUrl.replace("APPID", appid)
    # redirect需要用urlencode处理
    redirect_url = urllib.parse.quote(redirect_url)
    wechatUrl = wechatUrl.replace("REDIRECT_URI", redirect_url)

    wechatUrl = wechatUrl.replace("STATE", state)
    return wechatUrl


def getWebAccessToken(appid=None, appsecret=None, code=None):
    '''
    通过code来换取access_token和openid
    :param appid:
    :param appsecret:
    :param code:
    :return:
    '''
    wechatUrl = "https://api.weixin.qq.com/sns/oauth2/access_token?" \
                 "appid=APPID&secret=SECRET&code=CODE&grant_type=authorization_code"
    if appid is None:
        return "need appid"
    if appsecret is None:
        return "need appsecret"
    if code is None:
        return "need code"
    wechatUrl = wechatUrl.replace("APPID", appid)
    wechatUrl = wechatUrl.replace("SECRET", appsecret)
    wechatUrl = wechatUrl.replace("CODE", code)
    temReqJson = requests.get(wechatUrl)
    try:
        temReqPy = json.loads(temReqJson.text)
        temReqJson.close()
        print(temReqPy)
        return temReqPy
    finally:
        temReqJson.close()


def refreshAccessToken(appid=None, access_token=None):
    '''
    刷新access_token
    :param appid:
    :param access_token:
    :return:
    '''
    if appid is None:
        return "need appid"
    if access_token is None:
        return "need access_token"

    wechatUrl = "https://api.weixin.qq.com/sns/oauth2/refresh_token?" \
                "appid=APPID&grant_type=refresh_token&refresh_token=REFRESH_TOKEN"
    wechatUrl = wechatUrl.replace("APPID", appid)
    wechatUrl = wechatUrl.replace("REFRESH_TOKEN", access_token)
    temReq = requests.get(wechatUrl)
    try:
        newAccessToken = json.loads(temReq.text)
        temReq.close()
        print("access_token:", newAccessToken)
        return newAccessToken
    finally:
        temReq.close()


def getUserInfo(access_token=None, openid=None):
    '''
    在scope为snsapi_userinfo的情况下用access_token和openid来获取用户信息
    :param access_token:
    :param openid:
    :return:
    '''
    wechatUrl = "https://api.weixin.qq.com/sns/userinfo?access_token=ACCESS_TOKEN&openid=OPENID&lang=zh_CN"
    wechatUrl = wechatUrl.replace("ACCESS_TOKEN", access_token)
    wechatUrl = wechatUrl.replace("OPENID", openid)
    temReq = requests.get(wechatUrl)
    try:
        userInfo = json.loads(temReq.text)
        temReq.close()
        return userInfo
    finally:
        temReq.close()


def getAccessToken(appid=None, appsecret=None):
    '''
    获取接口授权凭证，access_token ，区别网页授权。
    1、有效期为2小时。
    2、需要定时刷新。
    3、建议方式：保存在服务器，然后定时刷新从新获取。（参考开发文档）
    :return:
    '''
    wechatUrl = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=APPID&secret=APPSECRET"
    wechatUrl = wechatUrl.replace("APPID", appid)
    wechatUrl = wechatUrl.replace("APPSECRET", appsecret)
    temReq = requests.get(wechatUrl)
    try:
        accessToken = json.loads(temReq.text)
        temReq.close()
        print("access_token:",accessToken)
        return accessToken
    finally:
        temReq.close()


'''
发送模板信息给某个用户步骤：
0、方式为post
1、获取access_token
2、需要openid（只支持单个用户发送）、模板ID、模板跳转链接以及模板内容。
'''


def setKeywordList(key0=None, key1=None, key2=None, key3=None, key4=None, key5=None, mark=None):
    color = "#173177"
    postData = {}
    if key0 is not None:
        postData["first"] = {'value':key0, "color":color}
    if key1 is not None:
        postData["keyword1"] = {'value':key1, "color":color}
    if key2 is not None:
        postData["keyword2"] = {'value':key2, "color":color}
    if key3 is not None:
        postData["keyword3"] = {'value':key3, "color":color}
    if key4 is not None:
        postData["keyword4"] = {'value':key4, "color":color}
    if key5 is not None:
        postData["keyword5"] = {'value':key5, "color":color}
    if mark is not None:
        postData["remark"] = {'value':mark, "color":color}

    return postData


def sendTemplateMessage(access_token, openid, templateMessageId, redirect_url, keywordList):
    '''
    发送模板信息给某个openid
    :param access_token:
    :param openid:
    :param templateMessageId:
    :param redirect_url:
    :param keywordList:
    :return:
    '''
    wechatUrl = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=ACCESS_TOKEN"
    wechatUrl = wechatUrl.replace("ACCESS_TOKEN", access_token)
    postData = {}
    postData["touser"] = openid
    postData["template_id"] = templateMessageId
    postData["url"] = redirect_url
    postData["data"] = keywordList
    print(postData)
    temReq = requests.post(wechatUrl, data=json.dumps(postData))
    try:
        sendAnswer = json.loads(temReq.text)
        temReq.close()
        print(sendAnswer)
        return sendAnswer
    finally:
        temReq.close()



def TimeCmp():
    '''
    时间对比，判断时间是否属于firsttime和secondtime两个之间
    节假日对比，判断是否为节假日
    :return:
    '''
    import datetime
    import requests
    firsttime = datetime.time(hour=8,minute=30)
    secondtime = datetime.time(hour=17, minute=0)
    now = datetime.datetime.now()
    nowtime = now.time()
    nowday = datetime.datetime(year=now.year,month=now.month,day=now.day).strftime("%Y%m%d")
    api = "http://tool.bitefu.net/jiari/?d=" + str(nowday)
    todaystate = requests.get(api).text
    if todaystate == '0':
        if (nowtime > firsttime) and (nowtime < secondtime):
            return '0'
        else:
            return '4'
    elif todaystate == '':
        return 0
    else:
        return todaystate
