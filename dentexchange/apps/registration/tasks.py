# -*- coding:utf-8 -*-
from celery.task import task

from django.contrib.auth.models import User
from django.template.loader import render_to_string as render_to_string_html
from django.template.loader import render_to_string as render_to_string_text
from django.template import RequestContext
from django.core.mail import EmailMultiAlternatives

from . import strings, constants


@task
def send_welcome_message(http_host, email):
    user = User.objects.get(email=email)
    html = render_to_string_html('registration/mail/welcome.html',
        dict(user=user, http_host=http_host))
    body = render_to_string_text('registration/mail/welcome.txt',
        dict(user=user, http_host=http_host))
    msg = EmailMultiAlternatives(strings.SEND_WELCOME_MESSAGE, body,
        constants.FROM_WELCOME_EMAIL, [email])
    msg.attach_alternative(html, 'text/html')
    msg.send()
