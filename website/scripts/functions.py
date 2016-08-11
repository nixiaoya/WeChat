#-*- coding=utf-8 -*-

import urllib
import urllib2
import socket
import json
import time

def getHttpStatus(obj):
    '''
    处理http请求和响应 
    '''
    mtime = lambda:int(round(time.time() *1000))
    header = { 
        'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:37.0) Gecko/20100101 Firefox/37.0'
    }       
    site = obj['site']
    req_url = obj['url']

    context = {
        'site':site,
        'log':'',
        'code':''
    }
    starts = mtime()

    req = urllib2.Request(req_url)

    try:
        resp = urllib2.urlopen(req, timeout=3)
    except urllib2.HTTPError as e:
        context['log'] = 'HttpError {0}'.format(e.code)
    except urllib2.URLError as e:
        context['log'] = 'URLError {0}'.format(e.reason)
    except socket.timeout as e:
        context['log'] = 'Timeout {0}'.format(str(e))
    else:
        context['code'] = resp.code 
        context['log'] = '{0} ms'.format(mtime() - starts)
    return context
