# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url

from src.apps.product import views

urlpatterns = [
    url(r'^$', views.CategoryListView.as_view(), name='list'),
    # url(r'^latest/$', views.TestView.as_view(), name='latest'),
    # url(r'^(?P<category_slug>[-\w]+)/$', views.TestView.as_view(), name='category-detail'),
    # url(r'^(?P<category_slug>[-\w]+)/(?P<product_slug>[-\w]+)$', views.TestView.as_view(), name='product-detail'),
]
