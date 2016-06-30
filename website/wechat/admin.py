from django.contrib import admin
from . import models

class KeyWords_Admin(admin.ModelAdmin):
    search_fields = ("keyword",)
    list_display = ("keyword", "content")
admin.site.register(models.KeyWords,KeyWords_Admin)

class FellowUser_Admin(admin.ModelAdmin):
    search_fields = ("userID",)
    list_display = ("userID",)
admin.site.register(models.FellowUser,FellowUser_Admin)

class Media_Admin(admin.ModelAdmin):
    search_fields = ("mType", "name")
    list_display = ("name", "mType", "mediaID")
admin.site.register(models.Media,Media_Admin)

class Title_Admin(admin.ModelAdmin):
    search_fields = ("title",)
    list_display = ("title","content")
admin.site.register(models.Title,Title_Admin)

class AccessToken_Admin(admin.ModelAdmin):
    search_fields = ("token",)
    list_display = ("token", "expires", "createAt", "wechatErrCode", "wechatErrMsg")
admin.site.register(models.AccessToken,AccessToken_Admin)

class MainMenu_Admin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display = ("name", "mType", "content")
admin.site.register(models.MainMenu,MainMenu_Admin)

class SubMenu_Admin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display = ("name", "mType", "mainMenu")
admin.site.register(models.SubMenu,SubMenu_Admin)