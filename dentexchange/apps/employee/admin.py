# -*- coding:utf-8 -*-
from django.contrib import admin
from django.conf import settings

from .models import EmployeeQuestionnaire, Resume
from .forms import ResumeForm
from . import strings


class EmployeeQuestionnaireAdmin(admin.ModelAdmin):
    list_display = ('get_email',)
    search_fields = ('user__email', 'user__userregistration__first_name',
        'user__userregistration__last_name',
        'user__userregistration__personal_address',
        'user__userregistration__personal_zip_code',
        'user__userregistration__personal_city',
        'user__userregistration__personal_state',
        'zip_code', 'city',
        'state', 'distance', 'schedule_type',
        'compensation_type', 'hourly_wage', 'experience_years', 'dental_school',
        'graduation_year', 'specific_strengths')
    fieldsets = (
        (None, {
            'fields': ('user',)
        }),
        (strings.ADMIN_JOB_POSITION, {
            'fields': ('job_position',)
        }),
        (strings.ADMIN_PRACTICE_TYPE, {
            'fields': ('solo_practitioner', 'multi_practitioner', 'corporate',)
        }),
        (strings.ADMIN_PATIENTS_PAYMENT_METHOD, {
            'fields': ('fee_for_service', 'insurance', 'capitation_medicaid',)
        }),
        (strings.ADMIN_LOCATION, {
            'fields': ('zip_code', 'city', 'state', 'distance',)
        }),
        (strings.ADMIN_SCHEDULE_TYPE, {
            'fields': ('schedule_type', 'monday_daytime', 'monday_evening',
            'tuesday_daytime', 'tuesday_evening', 'wednesday_daytime',
            'wednesday_evening', 'thursday_daytime', 'thursday_evening',
            'friday_daytime', 'friday_evening', 'saturday_daytime',
            'saturday_evening', 'sunday_daytime', 'sunday_evening',)
        }),
        (strings.ADMIN_COMPENSATION, {
            'fields': ('compensation_type', 'hourly_wage', 'annualy_wage',
            'production', 'collection',)
        }),
        (strings.ADMIN_EXPERIENCE, {
            'fields': ('experience_years',)
        }),
        (strings.ADMIN_EDUCATION, {
            'fields': ('dental_school', 'graduation_year',)
        }),
        (strings.ADMIN_VISA, {
            'fields': ('visa',)
        }),
        (strings.ADMIN_SPECIFIC_STRENGTHS, {
            'fields': ('specific_strengths',)
        }),
        (strings.ADMIN_VISIBILITY, {
            'fields': ('is_private',)
        }),
    )


class ResumeAdmin(admin.ModelAdmin):
    list_display = ('get_email', 'cv_file',)
    search_fields = ('user__email', 'user__userregistration__first_name',
        'user__userregistration__last_name',
        'user__userregistration__personal_address',
        'user__userregistration__personal_zip_code',
        'user__userregistration__personal_city',
        'user__userregistration__personal_state',
        'cv_file',)
    form = ResumeForm

    class Media(object):
        js = (
            '//ajax.googleapis.com/ajax/libs/jquery/{CDN_JQUERY_VERSION}/'
            'jquery.min.js'.format(**settings.CONTEXT_CONF),
        )


admin.site.register(EmployeeQuestionnaire, EmployeeQuestionnaireAdmin)
admin.site.register(Resume, ResumeAdmin)
