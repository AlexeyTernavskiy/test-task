# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.test import TestCase

from src.apps.product.factories import UserFactory, CategoryFactory, ProductFactory


class ProductModelTestCase(TestCase):
    def setUp(self):
        super(ProductModelTestCase, self).setUp()
        self.user = UserFactory()
        self.category = CategoryFactory()
        self.product = ProductFactory(user=self.user, category=self.category)

    def tearDown(self):
        super(ProductModelTestCase, self).tearDown()
        UserFactory.reset_sequence()
        CategoryFactory.reset_sequence()
        ProductFactory.reset_sequence()

    def test_create_category(self):
        self.assertEqual(self.category.name, 'category_name_0')
        self.assertEqual(self.category.slug, 'category_slug_0')
        self.assertEqual(self.category.description, 'category_description_0')

    def test_create_category_with_identical_unique_fields(self):
        data = {'slug': self.category.slug}
        self.assertRaises(IntegrityError, CategoryFactory, **data)

    def test_category__get_absolute_url(self):
        self.assertEqual(self.category.get_absolute_url(),
                         reverse('products:category-detail', args=[self.category.slug]))

    def test_category__str(self):
        self.assertEqual(self.category.__str__(), self.category.name)

    def test_create_product(self):
        self.assertEqual(self.product.user, self.user)
        self.assertEqual(self.product.category, self.category)
        self.assertEqual(self.product.name, 'product_name_0')
        self.assertEqual(self.product.slug, 'product_slug_0')
        self.assertEqual(self.product.description, 'product_description_0')
        self.assertEqual(self.product.price, 10)

    def test_create_product_with_identical_unique_fields(self):
        data = {'user': self.user, 'category': self.category, 'slug': self.product.slug}
        self.assertRaises(IntegrityError, ProductFactory, **data)

    def test_product__get_absolute_url(self):
        self.assertEqual(self.product.get_absolute_url(),
                         reverse('products:product-detail', args=[self.category.slug, self.product.slug]))

    def test_product__str(self):
        self.assertEqual(self.product.__str__(), self.product.name)
