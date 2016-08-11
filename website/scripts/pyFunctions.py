#-*- conding=utf-8 -*-
#!/bin/env python

from pymongo import MongoClient
from scripts.functions import getHttpStatus
from multiprocessing.dummy import Pool as ThreadPool

## db ##
mongo_db_client = MongoClient("mongodb://127.0.0.1:27017")
mdb = mongo_db_client['wechat']

#r = redis.Redis(host='127.0.0.1', port=6379)

## collection ##
command_list = 'commands'

def getCommandList():
    '''
    get command list
    '''
    resp = 'Commands='
    cmd_list = [x for x in mdb[command_list].find({},{'name':1}, limit=10, sort=[('name',1)]) if x['name'] != 'cmds']
    for cmd in cmd_list:
        if cmd == cmd_list[-1]:
            resp += '[{0}]'.format(cmd_list.index(cmd)) + cmd['name'] + ';'
        else:
            resp += '[{0}]'.format(cmd_list.index(cmd)) + cmd['name'] + ','
    return resp

def getSiteStatus():
    site_list = [ 
        {   
            'site':'onekp',
            'url':'https://www.bioinfodata.org/Blast4OneKP/'
        },
        {
            'site':'fish',
            'url':'http://www.fisht1k.org/'
        },
        {
            'site':'millet',
            'url':'http://db.cngb.org/millet/'
        },
        {
            'site':'b10k',
            'url':'https://www.bioinfodata.org/b10k/'
        }
    ] 
    resp = ''

    pool = ThreadPool(4)
    resp_list = pool.map(getHttpStatus, site_list)
    pool.close()
    pool.join()

    for site_resp in resp_list:
        resp += "{site_name}...... {log} [{code}]".format(site_name = site_resp['site'], log = site_resp['log'], code = site_resp['code']) + ';'
        
    return resp 
