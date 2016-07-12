# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from src.apps.product.models import CategoryModel, ProductModel


@admin.register(CategoryModel)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name',)


@admin.register(ProductModel)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    fields = ('user', 'category', 'name', 'slug', 'price', 'description',)
    list_display = ('name', 'category')
    list_filter = ('category',)
    ordering = ('name', 'category',)
