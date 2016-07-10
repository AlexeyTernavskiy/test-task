# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import factory
from django.contrib.auth import get_user_model

from src.apps.product.models import CategoryModel, ProductModel

User = get_user_model()
USER_PASSWORD = 'qwerty'


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username',)

    first_name = 'Homer'
    last_name = 'Simpson'
    username = factory.LazyAttribute(lambda n: '{0}{1}'.format(n.first_name,
                                                               n.last_name).lower())
    email = factory.LazyAttribute(lambda n: '{0}.{1}@example.com'.format(n.first_name,
                                                                         n.last_name).lower())
    password = factory.PostGenerationMethodCall('set_password', USER_PASSWORD)
    is_superuser = False
    is_staff = False
    is_active = True


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CategoryModel
        django_get_or_create = ('name',)

    name = factory.Sequence(lambda n: 'category_name_{}'.format(n))
    slug = factory.Sequence(lambda n: 'category_slug_{}'.format(n))
    description = factory.Sequence(lambda n: 'category_description_{}'.format(n))


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductModel
        django_get_or_create = ('name',)

    user = factory.SubFactory('src.apps.product.factories.UserFactory')
    category = factory.SubFactory('src.apps.product.factories.CategoryFactory')
    name = factory.Sequence(lambda n: 'product_name_{}'.format(n))
    slug = factory.Sequence(lambda n: 'product_slug_{}'.format(n))
    description = factory.Sequence(lambda n: 'product_description_{}'.format(n))
    price = factory.Sequence(lambda n: n + 10)
