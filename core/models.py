from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=255, null=True)
    number = models.IntegerField

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=30, blank=False, unique=True)
    slug = models.SlugField(max_length=288)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Seller(models.Model):
    user = models.OneToOneField(User, blank=False, null=False, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=False)
    email = models.CharField(max_length=255, null=False)
    county = models.CharField(max_length=255)
    number = models.IntegerField(unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE)
    posted_by = models.ForeignKey(Seller, related_name='seller', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    best_seller = models.BooleanField(default=False)
    top_rated = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Products'
        ordering = ('-created',)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(Customer, related_name='customer_order', on_delete=models.SET_NULL, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, blank=True, null=False)
    transaction_id = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.id


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    seller = models.ForeignKey(Seller, on_delete=models.SET_NULL, null=True, blank=True)
    number = models.IntegerField()
    address = models.CharField(max_length=255, null=True)
    county = models.CharField(max_length=255, null=True)
    country = models.CharField(max_length=255, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s %s' % (self.address, self.number)

