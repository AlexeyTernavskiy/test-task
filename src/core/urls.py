# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from allauth.account import views
from django.conf.urls import url, include
from django.contrib import admin

from src.core.views import IndexView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', views.login, name='account_login'),
    url(r'^logout/$', views.logout, name='account_logout'),
    url(r'^signup/$', views.signup, name='account_signup'),
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^products/', include('src.apps.product.urls', namespace='products'))
]
