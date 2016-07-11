# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.test import TestCase

from src.apps.product.factories import UserFactory, CategoryFactory, ProductFactory
from src.apps.product.models import CategoryModel, ProductModel


class ProductAdminTestCase(TestCase):
    def setUp(self):
        super(ProductAdminTestCase, self).setUp()
        self.user = UserFactory(is_superuser=True, is_staff=True)
        self.category = CategoryFactory()
        self.product = ProductFactory(user=self.user, category=self.category)
        self.client.force_login(user=self.user)

    def tearDown(self):
        super(ProductAdminTestCase, self).tearDown()
        UserFactory.reset_sequence()
        CategoryFactory.reset_sequence()
        ProductFactory.reset_sequence()
        self.client.logout()

    def category_data(self, name='Category Name', slug='category_slug', description='Category description'):
        return {
            'name': name,
            'slug': slug,
            'description': description
        }

    def product_data(self, pk=None, cat=None, name='Product Name', slug='product_slug', price=25,
                     description='Product description'):
        if pk is None:
            pk = self.user.pk
        if cat is None:
            cat = self.category.slug
        return {
            'user': pk,
            'category': cat,
            'name': name,
            'slug': slug,
            'price': price,
            'description': description
        }

    def test_admin_create_category(self):
        self.assertEquals(CategoryModel.objects.count(), 1)
        response = self.client.post(reverse('admin:product_categorymodel_add'), self.category_data())
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('admin:product_categorymodel_changelist'))
        self.assertEquals(CategoryModel.objects.count(), 2)

    def test_admin_update_category_name(self):
        self.assertEquals(CategoryModel.objects.count(), 1)
        new_category = CategoryFactory()
        self.assertEquals(CategoryModel.objects.count(), 2)
        self.assertEquals(new_category.name, 'category_name_1')
        response = self.client.post(reverse('admin:product_categorymodel_change', args=(new_category.slug,)),
                                    self.category_data(slug=new_category.slug,
                                                       description=new_category.description))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('admin:product_categorymodel_changelist'))
        self.assertEquals(CategoryModel.objects.count(), 2)
        self.assertEquals(CategoryModel.objects.get(slug=new_category.slug).name, 'Category Name')

    def test_admin_update_category_description(self):
        self.assertEquals(CategoryModel.objects.count(), 1)
        new_category = CategoryFactory()
        self.assertEquals(CategoryModel.objects.count(), 2)
        self.assertEquals(new_category.description, 'category_description_1')
        response = self.client.post(reverse('admin:product_categorymodel_change', args=(new_category.slug,)),
                                    self.category_data(name=new_category.name,
                                                       slug=new_category.slug))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('admin:product_categorymodel_changelist'))
        self.assertEquals(CategoryModel.objects.count(), 2)
        self.assertEquals(CategoryModel.objects.get(slug=new_category.slug).description, 'Category description')

    def test_admin_delete_category(self):
        self.assertEquals(CategoryModel.objects.count(), 1)
        new_category = CategoryFactory()
        self.assertEquals(CategoryModel.objects.count(), 2)
        self.assertEquals(ProductModel.objects.count(), 1)
        ProductFactory(user=self.user, category=new_category)
        self.assertEquals(ProductModel.objects.count(), 2)
        self.assertEquals(new_category.description, 'category_description_1')
        response = self.client.post(reverse('admin:product_categorymodel_delete', args=(new_category.slug,)),
                                    self.category_data(name=new_category.name,
                                                       slug=new_category.slug,
                                                       description=new_category.description))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('admin:product_categorymodel_changelist'))
        self.assertEquals(CategoryModel.objects.count(), 1)
        self.assertEquals(ProductModel.objects.count(), 1)
        self.assertEquals(CategoryModel.objects.get(name='category_name_0').description, 'category_description_0')

    def test_admin_create_category_with_identical_unique_fields(self):
        self.assertEquals(CategoryModel.objects.count(), 1)
        response = self.client.post(reverse('admin:product_categorymodel_add'),
                                    self.category_data(name=self.category.name,
                                                       slug=self.category.slug))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Category with this Name already exists.')
        self.assertContains(response, 'Category with this Url already exists.')
        self.assertEquals(CategoryModel.objects.count(), 1)
        self.assertEquals(CategoryModel.objects.get(name='category_name_0').description, 'category_description_0')

    def test_admin_update_category_with_identical_unique_field(self):
        self.assertEquals(CategoryModel.objects.count(), 1)
        new_category = CategoryFactory()
        self.assertEquals(CategoryModel.objects.count(), 2)
        self.assertEquals(new_category.description, 'category_description_1')
        response = self.client.post(reverse('admin:product_categorymodel_change', args=(new_category.slug,)),
                                    self.category_data(name=self.category.name))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Category with this Name already exists.')
        self.assertEquals(CategoryModel.objects.count(), 2)
        self.assertEquals(CategoryModel.objects.get(slug=new_category.slug).name, 'category_name_1')

    def test_admin_create_category_with_blank_fields(self):
        self.assertEquals(CategoryModel.objects.count(), 1)
        response = self.client.post(reverse('admin:product_categorymodel_add'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required.', 3)
        self.assertEquals(CategoryModel.objects.count(), 1)

    def test_admin_create_product(self):
        self.assertEquals(ProductModel.objects.count(), 1)
        response = self.client.post(reverse('admin:product_productmodel_add'),
                                    self.product_data())
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('admin:product_productmodel_changelist'))
        self.assertEquals(ProductModel.objects.count(), 2)

    def test_admin_update_product_name(self):
        self.assertEquals(ProductModel.objects.count(), 1)
        self.assertEqual(ProductModel.objects.get(slug=self.product.slug).name, 'product_name_0')
        response = self.client.post(reverse('admin:product_productmodel_change', args=(self.product.slug,)),
                                    self.product_data(slug=self.product.slug,
                                                      price=self.product.price,
                                                      description=self.product.description))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('admin:product_productmodel_changelist'))
        self.assertEquals(ProductModel.objects.count(), 1)
        self.assertEqual(ProductModel.objects.get(slug=self.product.slug).name, 'Product Name')

    def test_admin_update_product_price(self):
        self.assertEquals(ProductModel.objects.count(), 1)
        self.assertEqual(ProductModel.objects.get(slug=self.product.slug).price, 10)
        response = self.client.post(reverse('admin:product_productmodel_change', args=(self.product.slug,)),
                                    self.product_data(name=self.product.name,
                                                      slug=self.product.slug,
                                                      description=self.product.description))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('admin:product_productmodel_changelist'))
        self.assertEquals(ProductModel.objects.count(), 1)
        self.assertEqual(ProductModel.objects.get(slug=self.product.slug).price, 25)

    def test_admin_update_product_description(self):
        self.assertEquals(ProductModel.objects.count(), 1)
        self.assertEqual(ProductModel.objects.get(slug=self.product.slug).description, 'product_description_0')
        response = self.client.post(reverse('admin:product_productmodel_change', args=(self.product.slug,)),
                                    self.product_data(name=self.product.name,
                                                      slug=self.product.slug,
                                                      price=self.product.price))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('admin:product_productmodel_changelist'))
        self.assertEquals(ProductModel.objects.count(), 1)
        self.assertEqual(ProductModel.objects.get(slug=self.product.slug).description, 'Product description')

    def test_admin_delete_product(self):
        self.assertEquals(ProductModel.objects.count(), 1)
        response = self.client.post(reverse('admin:product_productmodel_delete', args=(self.product.slug,)),
                                    self.category_data(name=self.category.name,
                                                       slug=self.category.slug,
                                                       description=self.category.description))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('admin:product_productmodel_changelist'))
        self.assertEquals(ProductModel.objects.count(), 0)

    def test_admin_update_product_with_identical_unique_field(self):
        self.assertEquals(ProductModel.objects.count(), 1)
        new_product = ProductFactory(user=self.user, category=self.category)
        self.assertEquals(ProductModel.objects.count(), 2)
        self.assertEquals(new_product.description, 'product_description_1')
        response = self.client.post(reverse('admin:product_productmodel_change', args=(new_product.slug,)),
                                    self.category_data(name=self.category.name))
        self.assertEqual(response.status_code, 200)
        self.assertEquals(ProductModel.objects.count(), 2)
        self.assertEquals(ProductModel.objects.get(slug=new_product.slug).name, 'product_name_1')

    def test_admin_create_product_with_blank_fields(self):
        self.assertEquals(ProductModel.objects.count(), 1)
        response = self.client.post(reverse('admin:product_productmodel_add'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required.', 6)
        self.assertEquals(ProductModel.objects.count(), 1)
