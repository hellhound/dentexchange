# -*- coding:utf-8 -*-
from django.contrib.auth.decorators import user_passes_test

EMPLOYER = True
EMPLOYEE = False

def login_required_for(login_types):
    def check_is_employer(user):
        if not hasattr(user, 'userregistration'):
            return False
        if isinstance(login_types, bool):
            return user.userregistration.is_employer == login_types
        return any(map(lambda is_employer: \
            user.userregistration.is_employer == is_employer, login_types))
    return user_passes_test(check_is_employer)
