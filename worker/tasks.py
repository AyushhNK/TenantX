# tasks.py
from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_invite_email(email, reset_url, org_name):
    subject = f"You've been invited to join {org_name}"
    message = f"Hello, please set your password here: {reset_url}"
    send_mail(subject, message, "noreply@tenantx.com", [email])
