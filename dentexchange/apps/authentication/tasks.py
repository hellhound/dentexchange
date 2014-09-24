# -*- coding:utf-8 -*-
from celery.task import task

from django.contrib.auth.models import User
from django.template.loader import render_to_string as render_to_string_html
from django.template.loader import render_to_string as render_to_string_text
from django.template import RequestContext
from django.core.mail import EmailMultiAlternatives

from .models import RecoveryToken
from . import strings, constants


@task
def send_confirmation(http_host, email):
    user = User.objects.get(email=email)
    token = RecoveryToken.objects.create(user=user)
    html = render_to_string_html('authentication/mail/email_confirmation.html',
        dict(token=token, http_host=http_host))
    body = render_to_string_text('authentication/mail/email_confirmation.txt',
        dict(token=token, http_host=http_host))
    msg = EmailMultiAlternatives(strings.SEND_CONFIRMATION_SUBJECT, body,
        constants.FROM_PASSWORD_RECOVERY_EMAIL, [email])
    msg.attach_alternative(html, 'text/html')
    msg.send()
