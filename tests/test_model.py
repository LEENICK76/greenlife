from django.contrib.auth.models import User
from django.test import TestCase

from Products.models import Category, Product, Seller


class TestCategoryModel(TestCase):
    def setUp(self):
        self.data = Category.objects.create(name='greens', slug='greens')

    def test_category_model_entry(self):
        data = self.data
        self.assertTrue(isinstance(data, Category))
        self.assertEqual(str(data), 'greens')


class TestProductModel(TestCase):
    def setUp(self):
        Category.objects.create(name='greens', slug='greens')
        User.objects.create(username='admin')
        Seller.objects.create(user=User.objects.first(), name='Nick', email='lee@gmail.com', county='Nairobi', number=234)

        self.data = Product.objects.create(category_id=1, posted_by_id=1, name='greens', description='veges lovers',
                                           price=300, slug='greens')

    def test_product_model_entry(self):
        data = self.data
        self.assertTrue(isinstance(data, Product))
        self.assertEqual(str(data), data.name)

