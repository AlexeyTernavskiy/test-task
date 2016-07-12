# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from decimal import Decimal

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.validators import MinValueValidator, MinLengthValidator
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel


class BaseInfoMixin(models.Model):
    name = models.CharField(max_length=50,
                            unique=True,
                            verbose_name=_('Name'),
                            validators=[MinLengthValidator(limit_value=3)], )
    slug = models.SlugField(max_length=50,
                            unique=True,
                            primary_key=True,
                            verbose_name=_('Url'),
                            validators=[MinLengthValidator(limit_value=3)], )
    description = models.TextField(verbose_name=_('Description'),
                                   validators=[MinLengthValidator(limit_value=3)], )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class CategoryModel(BaseInfoMixin):
    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ('name',)

    def get_absolute_url(self):
        return reverse('products:category_detail', args=[self.slug])


@python_2_unicode_compatible
class ProductModel(BaseInfoMixin, TimeStampedModel):
    user = models.ForeignKey(User,
                             related_name='product',
                             verbose_name=_('User'), )
    category = models.ForeignKey(CategoryModel,
                                 related_name='product',
                                 verbose_name=_('Category'))
    price = models.DecimalField(verbose_name=_('Price'),
                                decimal_places=2,
                                max_digits=12,
                                validators=[MinValueValidator(Decimal('0.01'))], )

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
        ordering = ('name',)

    def get_absolute_url(self):
        return reverse('products:product_detail', args=[self.category.slug, self.slug])
