# -*- coding: utf-8 -*-

from django.views.generic import ListView

from src.apps.product.models import CategoryModel


class CategoryListView(ListView):
    template_name = 'pages/products.html'
    model = CategoryModel
    context_object_name = 'categories'
