# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, View, DetailView

from src.apps.product.models import CategoryModel, ProductModel


class TestView(View):
    pass


class CategoriesListView(ListView):
    template_name = 'pages/categories.html'
    model = CategoryModel
    context_object_name = 'categories'
    paginate_by = 3

    def get_queryset(self):
        return super(CategoriesListView, self).get_queryset().annotate(product_count=Count('product'))


class ProductsListView(ListView):
    template_name = 'pages/products.html'
    model = ProductModel
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        return super(ProductsListView, self).get_queryset().prefetch_related('category', 'user').filter(
            category_id=self.kwargs['category_slug'])

    def get_context_data(self, **kwargs):
        context = super(ProductsListView, self).get_context_data(**kwargs)
        context['category'] = CategoryModel.objects.get(slug=self.kwargs['category_slug']).name
        return context


class ProductDetailView(DetailView):
    template_name = 'pages/product.html'
    model = ProductModel
    context_object_name = 'product'

    def get_object(self):
        return get_object_or_404(ProductModel, slug=self.kwargs['product_slug'])


class LatestProductListView(ListView):
    template_name = 'pages/latest_product.html'
    model = ProductModel
    context_object_name = 'products'

    def get_queryset(self):
        return super(LatestProductListView, self).get_queryset().prefetch_related('category', 'user').filter(
            created__gte=(datetime.datetime.now() - datetime.timedelta(days=1))).order_by('-created')
