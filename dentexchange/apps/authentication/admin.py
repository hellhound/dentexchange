# -*- coding:utf-8 -*-
from django.contrib import admin

from .models import RecoveryToken


class RecoveryTokenAdmin(admin.ModelAdmin):
    list_display = ('get_email', 'token', 'timestamp')
    search_fields = ('token', 'timestamp')


admin.site.register(RecoveryToken, RecoveryTokenAdmin)
