from django.forms import ModelForm

from Products.models import Product


class ProductForm(ModelForm):
    def _init_(self, *args, **kwargs):
        super(ProductForm, self)._init_(*args, **kwargs)

    class Meta:
        model = Product
        fields = ['category', 'name', 'image', 'description', 'price']
