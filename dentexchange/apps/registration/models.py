# -*- coding:utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

from libs import constants as lib_constants
from . import strings
from . import constants


class UserRegistration(models.Model):
    ### User registration
    user = models.OneToOneField(User,
        verbose_name=strings.USER_REGISTRATION_USER)
    is_employer = models.BooleanField(
        verbose_name=strings.USER_REGISTRATION_ACCOUNT_TYPE,
        choices=constants.USER_REGISTRATION_IS_EMPLOYER_CHOICES,
        default=constants.USER_REGISTRATION_IS_EMPLOYER_CHOICES.EMPLOYER)
    ### Personal Info
    first_name = models.CharField(
        verbose_name=strings.USER_REGISTRATION_FIRST_NAME,
        max_length=100, blank=True)
    last_name = models.CharField(
        verbose_name=strings.USER_REGISTRATION_LAST_NAME,
        max_length=100, blank=True)
    personal_address = models.CharField(
        verbose_name=strings.USER_REGISTRATION_PERSONAL_ADDRESS,
        max_length=200, blank=True)
    personal_zip_code = models.DecimalField(
        verbose_name=strings.USER_REGISTRATION_ZIP_CODE,
        max_digits=5, decimal_places=0, blank=True, null=True)
    personal_city = models.CharField(
        verbose_name=strings.USER_REGISTRATION_CITY,
        max_length=100, blank=True)
    personal_state = models.CharField(
        verbose_name=strings.USER_REGISTRATION_STATE,
        choices=lib_constants.STATE_CHOICES,
        max_length=2, blank=True)

    class Meta(object):
        verbose_name = strings.USER_REGISTRATION_VERBOSE_NAME
        verbose_name_plural = strings.USER_REGISTRATION_VERBOSE_NAME_PLURAL

    def __unicode__(self):
        return self.user.email

    def get_email(self):
        return self.user.email
