from django.contrib.auth.models import User
from django.http import HttpRequest
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse

from Products.models import Category, Product, Seller


class TestViewResponse(TestCase):
    def setUp(self):
        self.c = Client()
        self.factory = RequestFactory()
        Category.objects.create(name='greens', slug='greens')
        User.objects.create(username='admin')
        Seller.objects.create(user=User.objects.first(), name='Nick', email='lee@gmail.com', county='Nairobi',
                              number=234)
        Product.objects.create(category_id=1, posted_by_id=1, name='greens', description='veges lovers',
                               price=300, slug='greens')

    def test_url_allowed_hosts(self):
        respose = self.c.get('/', HTTP_HOST='no-address.com')
        self.assertEqual(respose.status_code, 400)
        response = self.c.get('/', HTTP_HOST='your-domain.com')
        self.assertEqual(response.status_code, 200)

    # def test_category_url(self):
    #     response = self.c.get(reverse('core:category_list', args=['greens']))
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_product_detail_url(self):
    #     response = self.c.get(reverse('core:product_detail', args=['greens']))
    #     self.assertEqual(response.status_code, 200)

    # def test_homepage_html(self):
    #     request = HttpRequest()
    #     # response = products_all(request)
    #     html = response.content.decode('utf8')
    #     self.assertIn('Vegetables', html)
    #     self.assertEqual(response.status_code, 200)
