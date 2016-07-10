# -*- coding: utf-8 -*-
from django.contrib import admin

from src.apps.product.models import CategoryModel


@admin.register(CategoryModel)
class CategoryAdmin(admin.ModelAdmin):
    pass
