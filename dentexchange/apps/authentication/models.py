# -*- coding:utf-8 -*-
import hashlib
from uuid import uuid4
import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

from . import strings, constants


class RecoveryTokenManager(models.Manager):
    def is_token_valid(self, token):
        return bool(self.get_queryset().filter(
            token=token, timestamp__gte=now() - datetime.timedelta(
            days=constants.RECOVERY_EXPIRATION_TIME_DAYS)).count()
        )


class RecoveryToken(models.Model):
    user = models.ForeignKey(User, verbose_name=strings.RECOVERY_TOKEN_USER)
    timestamp = models.DateTimeField(
        verbose_name=strings.RECOVERY_TOKEN_TIMESTAMP,
        auto_now_add=True, editable=False)
    token = models.CharField(verbose_name=strings.RECOVERY_TOKEN_TOKEN,
        max_length=64, editable=False, unique=True)
    objects = RecoveryTokenManager()

    def save(self, *args, **kwargs):
        self.token = hashlib.sha256(unicode(uuid4())).hexdigest()
        super(RecoveryToken, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.token

    def get_email(self):
        return self.user.email
