# -*- coding:utf-8 -*-
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


class ModelEmailBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        model = get_user_model()
        try:
            user = model.objects.get(email=username)
            if user.check_password(password):
                return user
        except model.DoesNotExist:
            return None
        return None
