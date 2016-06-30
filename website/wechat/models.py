#coding=utf-8
from __future__ import unicode_literals

from django.db import models

class KeyWords(models.Model):
    '''
    用于和用户实时交互的关键词列表
    '''
    keyword = models.CharField(max_length=64, help_text=u'关键词')
    content = models.TextField(blank=True, help_text=u'关键词的响应信息') 

    def __unicode__(self):
        return self.keyword

class FellowUser(models.Model):
    '''
    关注的用户信息
    '''
    userID = models.CharField(max_length=64, help_text=u'用户的 openID')
    createAt = models.DateTimeField(auto_now_add=True, help_text=u'用户的创建时间')

    def __unicode__(self):
        return self.userID
        
class Media(models.Model):
    '''
    媒体资源信息
    '''
    type_choice = ((1,'pic'),(2,'music'),(3,'video'))
    mType = models.IntegerField(choices=type_choice, help_text=u'媒体数据类型')
    name = models.CharField(max_length=128, help_text=u'媒体数据名称')
    mediaID = models.CharField(max_length=64, help_text=u'媒体数据id')

    def __unicode__(self):
        return self.name

class Title(models.Model):
    '''
    推送文章
    '''
    title = models.CharField(max_length=128, help_text=u'文章标题')
    content = models.TextField(blank=True, help_text=u'文章主体')
    createAt = models.DateTimeField(auto_now_add=True, help_text=u'文章创建时间')

    def __unicode__(self):
        return self.title

class AccessToken(models.Model):
    token = models.CharField(max_length=1024, blank=True, help_text=u'从微信服务器获取的access_token的值')
    expires = models.CharField(max_length=64, blank=True, help_text=u'从对方服务器获取的超时时间')
    createAt = models.DateTimeField(auto_now_add=True, help_text=u'token 的刷新时间')
    wechatErrCode = models.CharField(max_length=64, blank=True, help_text=u'刷新时获取的对方服务器返回的状态码')
    wechatErrMsg = models.TextField(blank=True, help_text=u'刷新时获取的对方服务器返回的状态信息')

    def __unicode__(self):
        return self.token

class MainMenu(models.Model):
    '''
    一级菜单
    '''
    mType = models.CharField(max_length=64, blank=True, help_text=u'菜单类型')
    name = models.CharField(max_length=64, help_text=u'菜单名称')
    content = models.CharField(max_length=64, blank=True, help_text=u'菜单的触发属性')
    priority = models.IntegerField(default=0, help_text=u'菜单排序的优先级')

    def getContentType(self):
        cType = ''
        if self.mType == "click":
            cType = 'key'
        elif  self.mType == "view":
            cType = 'url'
        elif  self.mType == "scancode_push":
            cType = 'key'
        elif  self.mType == "scancode_waitmsg":
            cType = 'key'
        elif  self.mType == "pic_sysphoto":
            cType = 'key'
        elif  self.mType == "pic_photo_or_album":
            cType = 'key'
        elif  self.mType == "pic_weixin":
            cType = 'key'
        elif  self.mType == "location_select":
            cType = 'key'
        elif  self.mType == "media_id":
            cType = 'media_id'
        elif  self.mType == "view_limited":
            cType = 'media_id'
        return cType

    def __unicode__(self):
        return self.name

class SubMenu(models.Model):
    '''
    二级菜单
    '''
    mainMenu = models.ForeignKey(MainMenu, related_name='subMenu', help_text=u'子菜单所属的一级菜单')
    mType = models.CharField(max_length=64, blank=True, help_text=u'菜单类型')
    name = models.CharField(max_length=64, help_text=u'菜单名称')
    content = models.CharField(max_length=64, blank=True, help_text=u'菜单的触发属性')
    priority = models.IntegerField(default=0, help_text=u'子菜单排序的优先级')

    def getContentType(self):
        cType = ''
        if self.mType == "click":
            cType = 'key'
        elif  self.mType == "view":
            cType = 'url'
        elif  self.mType == "scancode_push":
            cType = 'key'
        elif  self.mType == "scancode_waitmsg":
            cType = 'key'
        elif  self.mType == "pic_sysphoto":
            cType = 'key'
        elif  self.mType == "pic_photo_or_album":
            cType = 'key'
        elif  self.mType == "pic_weixin":
            cType = 'key'
        elif  self.mType == "location_select":
            cType = 'key'
        elif  self.mType == "media_id":
            cType = 'media_id'
        elif  self.mType == "view_limited":
            cType = 'media_id'
        return cType

    def __unicode__(self):
        return self.name
