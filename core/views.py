import datetime
import json

from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from .models import *

# Create your views here.
from .utils import cookie_cart, cart_data, guest_order


def search(request):
    query = request.GET.get('query', '')
    product = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))

    return render(request, 'search.html', {'query': query, 'product': product})


def home(request):
    products = Product.objects.all()
    data = cart_data(request)
    order_items = data['order_items']
    order = data['order']
    cart_items = data['cart_items']

    context = {
        'products': products,
        'cart_items': cart_items,
        'order_items': order_items,
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

    else:
        customer, order = guest_order(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id
    print(order.get_cart_total)
    if total == float(order.get_cart_total):
        print('hello we going')
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
    response = {
        'Payment': 'Complete',
    }
    print(request.body)

    notify_vendor(request, order)
    notify_customer(request, order)
    return JsonResponse(response, safe=False)


def notify_vendor(request, order):
    mails = [x[0] for x in order.orderitem_set.all().values_list('product__posted_by__user__email') if
             x[0] != '']
    subject = 'You have an order'
    message = f'Hi, you have an order from {request.user.username}.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = mails
    send_mail(subject, message, email_from, recipient_list, fail_silently=False)


def notify_customer(request, order):
    subject = 'Order Complete'
    message = f'Hi, {request.user.username}. You successfully made an order.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [request.user.email]
    send_mail(subject, message, email_from, recipient_list, fail_silently=False)
