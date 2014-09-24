# -*- coding:utf-8 -*-
import mock

from django.contrib.admin.sites import AdminSite as BaseAdminSite
from django.contrib.admin import autodiscover as base_autodiscover
from django.contrib.admin import *


class AdminSite(BaseAdminSite):
    callbacks = []

    @classmethod
    def add_callbacks(cls, *callbacks):
        cls.callbacks.extend(callbacks)

    def index(self, request, extra_context=None):
        for callback in self.callbacks:
            callback(self, request, extra_context=extra_context)
        return super(AdminSite, self).index(
            request, extra_context=extra_context)


site = AdminSite()


@mock.patch('django.contrib.admin.site', site)
def autodiscover():
    base_autodiscover()
