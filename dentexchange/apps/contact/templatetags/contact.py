# -*- coding:utf-8 -*-
import urllib

from django import template
from django.template.loader import render_to_string
from django.conf import settings

from employee import strings as employee_strings
from employer import strings as employer_strings

register = template.Library()


@register.inclusion_tag('contact/contact_button.html')
def contact_button(user, obj):
    if user.userregistration.is_employer:
        subject = employer_strings.EMPLOYER_CONTACT_SUBJECT
        body = urllib.quote(
            render_to_string('contact/mail/employer_contact_body.txt',
            dict(http_host=settings.DOMAIN_NAME, pk=obj.pk,
            first_name=obj.user.userregistration.first_name,
            last_name=obj.user.userregistration.last_name)))
    else:
        subject = employee_strings.EMPLOYEE_CONTACT_SUBJECT
        body = urllib.quote(
            render_to_string('contact/mail/employee_contact_body.txt',
            dict(http_host=settings.DOMAIN_NAME, pk=obj.pk,
            user=user, company_name=obj.praxis.company_name)))
    return dict(user=user, subject=subject, body=body)
