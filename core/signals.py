from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from core.models import Order


@receiver(post_save, sender=Order)
def send_notification(sender, instance, created, **kwargs):
    if created:
        mails = [x[0] for x in instance.orderitem_set.all().values_list('product__posted_by__user__email') if
                 x[0] != '']
        subject = 'New Order'
        from_email = settings.DEFAULT_FROM_EMAIL
        text_content = 'You have a new order!'
        html_content = render_to_string('vendor.html')
        for mail in mails:
            to_email = mail
            msg = EmailMultiAlternatives(subject=subject, body=text_content, from_email=from_email, to=to_email)
            msg.attach_alternative(html_content, 'text/html')
            msg.send()
