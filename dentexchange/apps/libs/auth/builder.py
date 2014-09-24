# -*- coding:utf-8 -*-
from base64 import b64encode as salt_b64encode
from base64 import b64encode as sha1_b64encode

import hashlib
import random

from django.contrib.auth.models import User


class UserFactory(object):
    @staticmethod
    def _base64_random_salt():
        return salt_b64encode('%i' % random.randint(0, 2**64))

    @staticmethod
    def _base64_sha1(string):
        return sha1_b64encode(hashlib.sha1(string).digest())

    @staticmethod
    def _normalize_email(email):
        return email.replace('@', '_').replace('.', '_')

    @classmethod
    def get_username_from_email(cls, email):
        hashed_email = cls._base64_sha1(email)
        normalized_email = cls._normalize_email(email)
        return (normalized_email[:10] + cls._base64_random_salt()[:-10] \
            + hashed_email)[:30]

    @classmethod
    def user_exists(cls, email):
        hashed_email = cls.get_username_from_email(email)
        return User.objects.filter(username=hashed_email).count() > 0

    @classmethod
    def create_user(cls, email, password):
        user = User(username=cls.get_username_from_email(email), email=email)
        user.set_password(password)
        user.save()
        return user
