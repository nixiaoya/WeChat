#coding=utf-8
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.template import loader
from django.conf import settings
from xml.etree import ElementTree as ET
import time
import hashlib
import json

from wechat.functions import *

#from .models import Joke, Knowledge, Quote

def token_required(func):
    def _token_required(request):
        token = request.GET.get('token','').strip()
        if token and token == settings.TOKEN:
            return func(request)
        else:
            return error404(request)
    return _token_required

def error404(request):
    # context = {}
    # template = get_template("main/404.html")
    # html = template.render(context,request)
    return HttpResponse('[404] Not found', status=404)
    
def error500(request):
    # context = {}
    # template = get_template("main/500.html")
    # html = template.render(context,request)
    return HttpResponse('[500] Server error', status=500)

@csrf_exempt
def handlerGet(request):
        signature = request.GET.get('signature', '') 
        timestamp = request.GET.get('timestamp', '')
        nonce = request.GET.get('nonce', '')
        echostr = request.GET.get('echostr', '')

        token = settings.TOKEN 

        hashlist = [token, timestamp, nonce]
        hashlist.sort()
        halstr = ''.join([s for s in hashlist])
        halstr = hashlib.sha1(halstr).hexdigest()

        if halstr == signature:
            return HttpResponse(echostr)
        else:
            return error404(request)

@csrf_exempt
def handlerPost(request):
        str_xml = ET.fromstring(request.body)
        msgType = str_xml.findtext("MsgType")

        respContent = 'bye bye'
        if msgType == 'text':
            reqContent = str_xml.findtext("Content")
            respContent = reqContent[::-1]

        elif msgType == 'event':
            event = str_xml.findtext("Event")
            if event == "subscribe":
                respContent = u'欢迎关注: ' + settings.WECHAT_TITLE  + "\n" + \
                            u'这里提供了 bla bla bla ' + "\n" + \
                            u'bla bla bla '

        toUser = str_xml.findtext("FromUserName")
        fromUser = str_xml.findtext("ToUserName")
        nowtime = str(int(time.time()))

        context = {
            "toUser":toUser,
            "fromUser":fromUser,
            "nowtime":nowtime,
            "content":respContent
            }
        template = loader.get_template('text.xml')
        html = template.render(context, request)
        return HttpResponse(html)

@csrf_exempt
def  Main(request):
    if request.method == "GET":
        return handlerGet(request)    
    else:
        return handlerPost(request)

@token_required
def CustomizeMenu(requset):
    access_token = getAccessToken()
    url = settings.WECHAT_MENU_API
    params = {
        'access_token':access_token
        } 
    url = url + '?' + urllib.urlencode(params)
    menu = genMenu()
    context = {}

    respContent = getHttpResponse(url, menu)
    respContent = json.loads(respContent)
    context['wechat_error_code'] = respContent['errcode']
    context['wechat_error_msg'] = respContent['errmsg']

    return JsonResponse(context)