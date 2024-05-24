import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mynotes.settings')
django.setup()

from django.core.mail import send_mail

send_mail(
    'Test Email',
    'This is a test email.',
    'reshetuuak@yandex.ru',
    ['reshetuyak@gmail.com'],
    fail_silently=False,
)