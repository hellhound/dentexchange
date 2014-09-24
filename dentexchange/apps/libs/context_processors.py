# -*- coding:utf-8 -*-
from django.conf import settings


def conf(request):
    return getattr(settings, 'CONTEXT_CONF', {})


def debug(request):
    return dict(DEBUG=settings.DEBUG)
