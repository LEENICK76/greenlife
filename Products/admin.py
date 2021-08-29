from django.contrib import admin

# Register your models here.
from Products.models import Seller, Category, Product

admin.site.register(Seller)
admin.site.register(Category)
admin.site.register(Product)