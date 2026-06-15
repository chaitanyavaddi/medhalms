from django.conf import settings
from django.tasks import task
from django.template.loader import render_to_string

from core.email import send_email


@task()
def send_welcome_email(user_email):
    html = render_to_string(
        'emails/welcome.html', {
        'brand_color': settings.BRAND_PRIMARY,
    })
    send_email(user_email, 'Welcome', html)
