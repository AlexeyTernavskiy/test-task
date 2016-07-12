# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.core.urlresolvers import reverse
from django.template.defaultfilters import date, time
from django.test import TestCase
from django.utils import timezone

from src.apps.product.factories import UserFactory, CategoryFactory, ProductFactory


class ProductViewsTestCase(TestCase):
    def setUp(self):
        super(ProductViewsTestCase, self).setUp()
        self.user = UserFactory()
        self.category = CategoryFactory()
        self.product = ProductFactory(user=self.user, category=self.category)
        self.client.force_login(user=self.user)

    def tearDown(self):
        super(ProductViewsTestCase, self).tearDown()
        UserFactory.reset_sequence()
        CategoryFactory.reset_sequence()
        ProductFactory.reset_sequence()
        self.client.logout()

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/index.html')

    def test_list_without_of_categories(self):
        self.category.delete()
        response = self.client.get(reverse('products:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/categories.html')
        self.assertQuerysetEqual(response.context['categories'], [])

    def test_list_of_categories(self):
        response = self.client.get(reverse('products:list'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['categories'], ['<CategoryModel: category_name_0>'])

    def test_count_product_in_category(self):
        ProductFactory.create_batch(size=5, user=self.user, category=self.category)
        response = self.client.get(reverse('products:list'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['categories'], ['<CategoryModel: category_name_0>'])
        self.assertEqual(response.context['categories'][0].product_count, 6)

    def test_show_fields_on_category_page(self):
        response = self.client.get(reverse('products:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.category.name)
        self.assertContains(response, self.category.slug)
        self.assertContains(response, self.category.description)

    def test_list_of_categories_with_pagination(self):
        CategoryFactory.create_batch(size=12)
        for page in range(1, 7):
            url = reverse('products:list') + '?page={}'.format(page)
            response = self.client.get(url)
            if page == 6:
                self.assertEqual(response.status_code, 404)
                self.assertTemplateUsed(response, '404.html')
                break
            self.assertEqual(response.status_code, 200)
            if page < 5:
                self.assertEqual(len(response.context['categories']), 3)
            else:
                self.assertEqual(len(response.context['categories']), 1)

    def test_category_url(self):
        self.assertEqual(self.category.get_absolute_url(),
                         reverse('products:category_detail', args=(self.category.slug,)))

    def test_list_without_of_products(self):
        self.product.delete()
        response = self.client.get(reverse('products:category_detail', args=(self.category.slug,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/products.html')
        self.assertQuerysetEqual(response.context['products'], [])

    def test_list_of_products_in_category_detail(self):
        ProductFactory.create_batch(size=1, user=self.user, category=self.category)
        response = self.client.get(reverse('products:category_detail', args=(self.category.slug,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/products.html')
        self.assertQuerysetEqual(response.context['products'], ['<ProductModel: product_name_0>',
                                                                '<ProductModel: product_name_1>'])
        for product in response.context['products']:
            self.assertEqual(product.category, self.category)

    def test_display_fields_on_products_page(self):
        response = self.client.get(reverse('products:category_detail', args=(self.category.slug,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)
        self.assertContains(response, self.product.slug)
        self.assertContains(response, self.product.price)
        self.assertContains(response, self.product.description)

    def test_nonexistent_products(self):
        response = self.client.get(reverse('products:category_detail', args=('nonexistent_url',)))
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')

    def test_list_of_products_with_pagination(self):
        ProductFactory.create_batch(size=26, user=self.user, category=self.category)
        for page in range(1, 5):
            url = reverse('products:category_detail', args=(self.category.slug,)) + '?page={}'.format(page)
            response = self.client.get(url)
            if page == 4:
                self.assertEqual(response.status_code, 404)
                self.assertTemplateUsed(response, '404.html')
                break
            self.assertEqual(response.status_code, 200)
            if page < 3:
                self.assertEqual(len(response.context['products']), 10)
            else:
                self.assertEqual(len(response.context['products']), 7)

    def test_product_url(self):
        self.assertEqual(self.product.get_absolute_url(),
                         reverse('products:product_detail', args=(self.product.category.slug, self.product.slug)))

    def test_product_detail(self):
        response = self.client.get(
            reverse('products:product_detail', args=(self.product.category.slug, self.product.slug)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/product.html')
        self.assertAlmostEqual(response.context['product'], self.product)
        self.assertAlmostEqual(response.context['product'].category, self.category)

    def test_display_fields_on_product_page(self):
        response = self.client.get(
            reverse('products:product_detail', args=(self.product.category.slug, self.product.slug)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)
        self.assertContains(response, self.product.price)
        self.assertContains(response, self.product.category)
        self.assertContains(response, self.product.user.username)
        self.assertContains(response, date(self.product.created))
        self.assertContains(response, time(self.product.created))
        self.assertContains(response, self.product.category.slug)

    def test_nonexistent_product(self):
        response = self.client.get(reverse('products:product_detail', args=('nonexistent_url', self.product.slug)))
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')
        response = self.client.get(reverse('products:product_detail', args=(self.category.slug, 'nonexistent_url')))
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')

    def test_latest_product_unauth(self):
        self.client.logout()
        redirect_url = reverse('account_login') + '?next={}'.format(reverse('products:latest'))
        response = self.client.get(reverse('products:latest'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)
        response = self.client.get(response.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_latest_product_auth(self):
        response = self.client.get(reverse('products:latest'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/latest_product.html')
        self.assertQuerysetEqual(response.context['products'], ['<ProductModel: product_name_0>'])

    def test_latest_product_added_after_24_hours(self):
        create_time = timezone.now() + datetime.timedelta(days=-1)
        self.product.created = create_time
        self.product.save()
        response = self.client.get(reverse('products:latest'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/latest_product.html')
        self.assertQuerysetEqual(response.context['products'], [])
