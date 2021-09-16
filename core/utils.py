import json

from Products.models import Product
from core.models import Order, OrderItem, Customer


def cookie_cart(request):
    try:
        try:
            cart_guest = json.loads(request.COOKIES['cart'])
        except:
            cart_guest = {}

        customer = {}
        order_items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cart_items = order['get_cart_items']

        for i in cart_guest:
            cart_items += cart_guest[i]['quantity']

            product = Product.objects.get(id=i)
            total = (product.price * cart_guest[i]['quantity'])

            order['get_cart_items'] += cart_guest[i]['quantity']
            order['get_cart_total'] += total
            print('mbogooooo')
            print(order['get_cart_total'])
            print(total)

            order_item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'imageURL': product.imageURL
                },
                'quantity': cart_guest[i]['quantity'],
                'get_total': total
            }
            order_items.append(order_item)
            print(customer)
    except:
        pass
    return {'order_items': order_items, 'order': order, 'cart_items': cart_items}


def cart_data(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        print(customer)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        order_items = order.orderitem_set.all()
        cart_items = order.get_cart_items
    else:
        cookie_data = cookie_cart(request)
        order_items = cookie_data['order_items']
        order = cookie_data['order']
        cart_items = cookie_data['cart_items']

    return {'order_items': order_items, 'order': order, 'cart_items': cart_items}


def guest_order(request, data):
    print('User not logged in')
    print(request.COOKIES)
    print(data)
    name = data['form']['name']
    email = data['form']['email']
    phone = data['form']['phone']

    cookie_data = cookie_cart(request)
    order_items = cookie_data['order_items']

    customer, created = Customer.objects.get_or_create(number=phone)
    customer.name = name
    customer.email = email
    customer.save()

    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    for item in order_items:
        product = Product.objects.get(id=item['product']['id'])

        order_item = OrderItem.objects.create(
            order=order,
            product=product,
            quantity=item['quantity']
        )
    return customer, order
