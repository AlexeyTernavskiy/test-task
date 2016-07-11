# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url

from src.apps.product import views

urlpatterns = [
    url(r'^$', views.CategoriesListView.as_view(), name='list'),
    url(r'^latest/$', views.TestView.as_view(), name='latest'),
    url(r'^(?P<category_slug>[-\w]+)/$', views.ProductsListView.as_view(), name='category_detail'),
    url(r'^(?P<category_slug>[-\w]+)/(?P<product_slug>[-\w]+)/$', views.ProductDetailView.as_view(),
        name='product_detail'),
]
