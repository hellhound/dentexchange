# -*- coding:utf-8 -*-
from functools import wraps
import datetime

from django.utils.decorators import available_attrs
from django.shortcuts import redirect
from django.utils.timezone import now

from .models import Membership
from . import constants


def enforce_membership(view_func):
    @wraps(view_func, assigned=available_attrs(view_func))
    def wrapped_view(request, *args, **kwargs):
        try:
            membership = request.user.membership
        except (Membership.DoesNotExist, AttributeError):
            return redirect('membership:home')
        if membership.plan_type.duration_unit != \
                constants.DURATION_UNIT_CHOICES.UNLIMITED \
                and membership.end_date < now():
            return redirect('membership:home')
        response = view_func(request, *args, **kwargs)
        response['CURRENT'] = True
        return response
    return wrapped_view
