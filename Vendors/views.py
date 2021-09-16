from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render, redirect

# Create your views here.
from django.utils.text import slugify

from Products.models import Seller, Product
from Vendors.forms import ProductForm, ProductRequestForm
from Vendors.models import ProductRequest
from accounts.forms import FarmerForm


@login_required
def become_farmer(request):
    user = request.user
    seller = Seller.objects.filter(user=user)
    if not seller:
        if request.method == 'POST':
            form = FarmerForm(request.POST)
            if form.is_valid():
                county = form.cleaned_data['county']
                name = form.cleaned_data['name']
                number = form.cleaned_data['number']
                user = request.user
                print(user)
                Seller.objects.create(
                    user=request.user,
                    name=name,
                    county=county,
                    number=number,
                    email=request.user.email,
                )
                return redirect('admin-farmer')

        else:
            form = FarmerForm()
    else:
        messages.success(request, "You're already a farmer")
        return redirect('admin-farmer')
    return render(request, 'vendor.html', {'form': form})


@login_required
def admin_farmer(request):
    farmer = request.user.seller
    products = Product.objects.filter(posted_by=farmer)
    return render(request, 'farmer_area.html', {'farmer': farmer, 'products': products})


@login_required
def add_product(request):
    user = request.user
    seller = Seller.objects.filter(user=user)
    if seller:
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES)
            if form.is_valid():
                product = form.save(commit=False)
                product.posted_by = request.user.seller
                product.slug = slugify(product.name)
                product.save()
                return redirect('admin-farmer')
        else:
            form = ProductForm()
    else:
        messages.warning(request, 'Sign Up to be a farmer first')
        return redirect('become-farmer')
    return render(request, 'add-product.html', {'form': form})


@login_required
def make_product_request(request):
    customer = request.user.customer
    if customer:
        if request.method == 'POST':
            form = ProductRequestForm(request.POST)
            if form.is_valid():
                category = form.cleaned_data['category']
                name = form.cleaned_data['name']
                description = form.cleaned_data['description']
                ProductRequest.objects.create(
                    customer=customer,
                    category=category,
                    name=name,
                    description=description,
                )
                return redirect('my-request')
        else:
            form = ProductRequestForm()
    else:
        messages.warning(request, 'Login to make requests')
        return redirect('login')
    return render(request, 'add-request.html', {'form': form})


@login_required
def my_requests(request):
    user = request.user
    if user.is_authenticated:
        customer = user.customer
        product = ProductRequest.objects.filter(customer=customer)
    else:
        messages.warning(request, 'Login first')
        return redirect('login')

    return render(request, 'my-requests.html', {'product': product})
