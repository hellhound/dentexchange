# -*- coding:utf-8 -*-
from django.contrib import admin

from .models import UserRegistration
from . import strings


class UserRegistrationAdmin(admin.ModelAdmin):
    list_display = ('get_email', 'is_employer',)
    list_filter = ('is_employer',)
    search_fields = ('user__email', 'first_name', 'last_name',
        'personal_address', 'personal_zip_code', 'personal_city',
        'personal_state')
    fieldsets = (
        (None, {
            'fields': ('user', 'is_employer',)
        }),
        (strings.ADMIN_PERSONAL_INFO, {
            'fields': ('first_name', 'last_name', 'personal_address',
                'personal_zip_code', 'personal_city', 'personal_state',)
        }),
    )


admin.site.register(UserRegistration, UserRegistrationAdmin)
