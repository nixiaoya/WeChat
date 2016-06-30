from django.conf.urls import url, include

from wechat import views

urlpatterns = [
	url(r'customize_menu', views.CustomizeMenu),
    url(r'^$', views.Main),
]
