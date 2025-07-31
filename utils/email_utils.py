from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

def send_order_email(user_email, subject, template, context):
    message = render_to_string(template, context)
    send_mail(
        subject,
        '',
        from_email=None,
        recipient_list=[user_email],
        html_message=message,
        fail_silently=False,
    )


def send_otp_email(user, otp, email):
    subject = "🔐 Verify Your Email with OTP – Action Required"
    context = {
        "user": user,
        "otp": otp
    }
    message = render_to_string("emails/otp_email.txt", context)

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False
    )


def send_new_otp_email(user, otp, email):
    subject = "🔄 Your New OTP Code"
    context = {
        "user": user,
        "otp": otp,
    }
    message = render_to_string("emails/new_otp_email.txt", context)

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )