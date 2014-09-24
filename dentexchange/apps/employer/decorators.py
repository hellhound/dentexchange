# -*- coding:utf-8 -*-
from functools import wraps

from django.utils.decorators import available_attrs
from django.shortcuts import redirect

from .models import Business


def enforce_business(view_func):
    @wraps(view_func, assigned=available_attrs(view_func))
    def wrapped_view(request, *args, **kwargs):
        try:
            business = request.user.business
        except Business.DoesNotExist:
            return redirect('employer:business')
        return view_func(request, *args, **kwargs)
    return wrapped_view
