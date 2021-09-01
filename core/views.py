import datetime
import json

from django.http import JsonResponse
from django.shortcuts import render
from .models import *


# Create your views here.
from .utils import cookie_cart, cart_data


def home(request):
    products = Product.objects.all()
    data = cart_data(request)
    order_items = data['order_items']
    order = data['order']
    cart_items = data['cart_items']

    context = {
        'products': products,
        'cart_items': cart_items,
        'order_items': order_items
    }
    return render(request, 'core/home.html', context=context)


def cart(request):
    data = cart_data(request)
    order_items = data['order_items']
    order = data['order']
    cart_items = data['cart_items']

    context = {'order_items': order_items, 'order': order, 'cart_items': cart_items}
    return render(request, 'core/cart.html', context=context)


def checkout(request):
    data = cart_data(request)
    order_items = data['order_items']
    order = data['order']
    cart_items = data['cart_items']

    context = {'order_items': order_items, 'order': order, 'cart_items': cart_items}
    return render(request, 'core/checkout.html', context=context)


def update_item(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('product', productId)
    print('action:', action)

    customer = request.user.customer
    product = Product.objects.get(id=productId)

    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        order_item.quantity = (order_item.quantity + 1)
    elif action == 'removed':
        order_item.quantity = (order_item.quantity - 1)

    order_item.save()

    if order_item.quantity <= 0:
        order_item.delete()
    return JsonResponse('Item was added', safe=False)


def process_order(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()

        if order.complete:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                number=customer.number,
                address=data['shippingInfo']['address'],
                county=data['shippingInfo']['county'],
                country=data['shippingInfo']['country'],
            )
    else:
        print('User not logged in')
        print(request.COOKIES)
        print(data)
        name = data['form']['name']
        email = data['form']['email']
        phone = data['form']['phone']
        print(name)
    response = {
        'Payment': 'Complete',
    }
    print(request.body)
    return JsonResponse(response, safe=False)
