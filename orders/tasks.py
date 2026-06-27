from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_welcome_email_task(user_email):
    subject = "Welcome to our site"
    message = "signed up successfully"
    from_email = settings.EMAIL_HOST_USER if hasattr(settings, "EMAIL_HOST_USER") else "webmaster@localhost"

    send_mail(subject, message, from_email, [user_email])
    return f"Welcome email sent to {user_email}"


@shared_task
def send_order_confirmation_task(user_email, order_id, total_price):
    subject = f"approve order #{order_id}"
    message = f"your order with number #{order_id} and price {total_price}, is set"
    from_email = settings.EMAIL_HOST_USER if hasattr(settings, "EMAIL_HOST_USER") else "webmaster@loalhost"
    send_mail(subject, message, from_email, [user_email])
    return f"Order confirmation email sent for order {order_id}"