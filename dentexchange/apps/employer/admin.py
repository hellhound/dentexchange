# -*- coding:utf-8 -*-
from django.contrib import admin

from libs import admin
from .models import Business, Praxis, JobPosting
from . import strings


class BusinessAdmin(admin.ModelAdmin):
    list_display = ('get_email', 'number_offices', 'is_mso',
        'number_employees',)
    search_fields = ('user__email', 'user__userregistration__first_name',
        'user__userregistration__last_name',
        'user__userregistration__personal_address',
        'user__userregistration__personal_zip_code',
        'user__userregistration__personal_city',
        'user__userregistration__personal_state',
        'number_offices', 'is_mso', 'number_employees',)
    list_filter = ('number_offices', 'is_mso', 'number_employees',)


class PraxisAdmin(admin.ModelAdmin):
    list_display = ('get_email', 'company_name',)
    search_fields = ('company_name', 'contact_first_name', 'contact_last_name',
        'address', 'zip_code', 'city', 'state', 'solo_practitioner',
        'multi_practitioner', 'corporate', 'fee_for_service', 'insurance',
        'capitation_medicaid',)
    list_filter = ('solo_practitioner', 'multi_practitioner', 'corporate',
        'fee_for_service', 'insurance', 'capitation_medicaid',)
    fieldsets = (
        (None, {
            'fields': ('business', 'is_active',)
        }),
        (strings.ADMIN_CONTACT_INFO, {
            'fields': ('company_name', 'contact_first_name',
            'contact_last_name',)
        }),
        (strings.ADMIN_PRAXIS_LOCATION, {
            'fields': ('address', 'zip_code', 'city', 'state',)
        }),
        (strings.ADMIN_PRACTICE_TYPE, {
            'fields': ('solo_practitioner', 'multi_practitioner', 'corporate',)
        }),
        (strings.ADMIN_PATIENTS_PAYMENT_METHOD, {
            'fields': ('fee_for_service', 'insurance', 'capitation_medicaid',)
        }),
    )


class JobPostingAdmin(admin.ModelAdmin):
    list_display = ('position_name', 'posting_title',)
    search_fields = ('position_name', 'posting_title', 'job_position',
        'schedule_type', 'monday_daytime', 'monday_evening', 'tuesday_daytime',
        'tuesday_evening', 'wednesday_daytime', 'wednesday_evening',
        'thursday_daytime', 'thursday_evening', 'friday_daytime',
        'friday_evening', 'saturday_daytime', 'saturday_evening',
        'sunday_daytime', 'sunday_evening', 'compensation_type', 'hourly_wage',
        'annualy_wage', 'experience_years', 'benefit_1', 'benefit_2',
        'benefit_3', 'benefit_4', 'benefit_5', 'benefit_6', 'benefit_other',
        'benefit_other_text', 'additional_comments', 'is_posted',)
    list_filter = ('schedule_type', 'monday_daytime', 'monday_evening',
        'tuesday_daytime', 'tuesday_evening', 'wednesday_daytime',
        'wednesday_evening', 'thursday_daytime', 'thursday_evening',
        'friday_daytime', 'friday_evening', 'saturday_daytime',
        'saturday_evening', 'sunday_daytime', 'sunday_evening',
        'compensation_type', 'hourly_wage', 'annualy_wage', 'experience_years',
        'benefit_1', 'benefit_2', 'benefit_3', 'benefit_4', 'benefit_5',
        'benefit_6', 'benefit_other',)
    fieldsets = (
        (None, {
            'fields': ('praxis', 'is_posted', 'is_active',)
        }),
        (strings.ADMIN_GENERAL_INFO, {
            'fields': ('position_name', 'posting_title',)
        }),
        (strings.ADMIN_JOB_POSTING_OFFERED, {
            'fields': ('job_position',)
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
        (strings.ADMIN_EXPERIENCE_REQUIRED, {
            'fields': ('experience_years',)
        }),
        (strings.ADMIN_BENEFITS_BEING_OFFERED, {
            'fields': ('benefit_1', 'benefit_2', 'benefit_3', 'benefit_4',
            'benefit_5', 'benefit_6', 'benefit_other', 'benefit_other_text',)
        }),
    )


admin.site.add_callbacks(
    lambda sender, request, **kwargs: Praxis.show_inactive(),
    lambda sender, request, **kwargs: JobPosting.show_inactive())
admin.site.register(Business, BusinessAdmin)
admin.site.register(Praxis, PraxisAdmin)
admin.site.register(JobPosting, JobPostingAdmin)
