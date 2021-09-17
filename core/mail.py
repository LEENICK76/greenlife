from django.conf import settings


def notify_vendor(order):
    from_email = settings.EMAIL_HOST_USER
    customer_order = order.customer
    # mails =