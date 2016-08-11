#coding=utf-8

from django.conf import settings
from django.utils import timezone

import subprocess
import urllib2
import urllib
import json
import time
import os

from wechat.models import MainMenu, SubMenu, AccessToken
from scripts.pyFunctions import *

class MyException(Exception):
    pass

def getHttpResponse(req_url, req_data={}):
    ''' 
    处理http请求和响应 
    '''
    header = { 
        'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:37.0) Gecko/20100101 Firefox/37.0'
        }    
    if req_data:
        req_data = urllib.urlencode(req_data)
        req = urllib2.Request(req_url, req_data, header)
    else:
        req = urllib2.Request(req_url)

    try:
        resp = urllib2.urlopen(req, timeout=5)
    except urllib2.HTTPError as e:
        raise MyException("HttpError: code=>%s reason=>%s" % (e.code,e.reason))
    except urllib2.URLError as e:
        raise MyException("URLError: %s" % e.reason)
    except socket.timeout as e:
        raise MyException("Socket timeout:%s" % e)
    else:
        return resp.read()

def requestNewToken():
    url = settings.WECHAT_TOKEN_API

    params = {
        'grant_type':'client_credential',
        'appid':settings.APPID,
        'secret':settings.SECRET
    }

    url = url + "?" + urllib.urlencode(params)
    resp = getHttpResponse(url)

    return json.loads(resp)

def getAccessToken():
    access_token = ''
    current_time = timezone.now()

    if AccessToken.objects.exclude(token='').exists():
        newest_token = AccessToken.objects.exclude(token='').order_by('-createAt')[0]
        if (current_time - newest_token.createAt).seconds < int(newest_token.expires):
            access_token = newest_token.token
            return access_token

    fresh_token = requestNewToken()
    if fresh_token.has_key("access_token"):
        access_token = fresh_token['access_token']
        new_access_token = AccessToken(
                token = fresh_token['access_token'],
                expires = fresh_token['expires_in']
            )
    else:
        new_access_token = AccessToken(
                wechatErrCode = fresh_token['errcode'],
                wechatErrMsg = fresh_token['errmsg']
            )
    new_access_token.save()

    if not access_token:
        raise ValueError('Acess Token error')

    return access_token

def genMenu():
    '''
    生成自定义的菜单列表
    '''
    menu = {}
    menu['button'] = []
    main_menu = MainMenu.objects.order_by('-priority')

    for main_bt in main_menu:
        layer1_button= {}
        layer1_button['name'] = main_bt.name

        if main_bt.subMenu.exists():
            layer1_button['sub_button'] = []
            sub_menu = main_bt.subMenu.order_by(-'priority')

            for sub_bt in sub_menu:
                layer2_button = {}
                layer2_button['name'] = sub_bt.name
                layer2_button['type'] = sub_bt.mType
                layer2_button[sub_bt.getContentType()] = sub_bt.content

                layer1_button['sub_button'].append(layer2_button)
        else:
            layer1_button['type'] = main_bt.mType
            layer1_button[main_bt.getContentType()] = main_bt.content

        menu['button'].append(layer1_button)
    return menu

def parseScriptOut(str_):
    '''
    format script output information
    '''
    resp = ''
    if str_.find(';') != -1:
        if str_.find('=') != -1:
            info_list = [ x.split('=') for x in str_.strip().split(";") if x != '']
        else:
            info_list = str_.strip().split(';')

        for info in info_list: 
            if type(info) == list:
                key = info[0].strip()
                value = info[1].strip()
                if value.find(',') != -1:
                    value = '\n'.join([x.strip() for x  in value.split(',')])
                resp += key + '\n' + value + '\n\n'
            else:
                resp += info + '\n'
    else:
        resp = str_
    return resp 
        

def execCommand(script_type, script):
    '''
    execute shell / python script
    '''
    resp = ''
    
    if script_type == 'function':
        func_resp = eval('{0}()'.format(script))
        try:
            func_resp = eval('{0}()'.format(script))
        except Exception as e:
            resp += 'Script error: {0}'.format(e)
        else:
            resp = parseScriptOut(func_resp)

    else:
        script_path = os.path.join(settings.SCRIPTS_ROOT, script)

        if os.path.isfile(script_path):
            if script_type == 'shell':
                (stdout, stderr) = subprocess.Popen(script_path, stdout=subprocess.PIPE, shell=True).communicate()
                if not stderr:
                    resp = parseScriptOut(stdout)
                else:
                    resp = 'Script error: {0}'.format(stderr)
            elif script_type == 'python':
                pass
        else:
            resp += 'Script error: script file not found.'
    return resp
    
