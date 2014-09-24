# -*- coding:utf-8 -*-
from django.db import models

from libs import constants as libs_constants
from libs.models.indexable import IndexableModel
import strings


class ZipCode(IndexableModel):
    code = models.DecimalField(
        verbose_name=strings.ZIP_CODE_CODE,
        max_digits=5, decimal_places=0,
        unique=True, db_index=True)
    city = models.CharField(
        verbose_name=strings.ZIP_CODE_CITY,
        max_length=100)
    state = models.CharField(
        verbose_name=strings.ZIP_CODE_STATE,
        choices=libs_constants.STATE_CHOICES,
        max_length=2)
    latitude = models.DecimalField(
        verbose_name=strings.ZIP_CODE_LATITUDE,
        max_digits=6, decimal_places=3)
    longitude = models.DecimalField(
        verbose_name=strings.ZIP_CODE_LONGITUDE,
        max_digits=6, decimal_places=3)

    class Meta(object):
        verbose_name = strings.ZIP_CODE_VERBOSE_NAME
        verbose_name_plural = strings.ZIP_CODE_VERBOSE_NAME_PLURAL

    def __unicode__(self):
        return unicode(self.code)
