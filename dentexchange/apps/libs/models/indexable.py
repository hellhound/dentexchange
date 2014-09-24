# -*- coding:utf-8 -*-
from django.db import models


class IndexableModel(models.Model):
    updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta(object):
        abstract = True
