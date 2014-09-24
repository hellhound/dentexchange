# -*- coding:utf-8 -*-
from django.contrib import admin

from .models import Plan, PlanPrice, Membership, Coupon
from . import strings


class PlanPriceInline(admin.TabularInline):
    model = PlanPrice
    extra = 1


class PlanAdmin(admin.ModelAdmin):
    list_display = ('title', 'for_employer')
    list_filter = ('for_employer',)
    search_fields = ('title', 'for_employer', 'content_description',
        'planprice__price', 'planprice__tag', 'planprice__is_free',
        'planprice__duration_magnitude', 'planprice__number_job_postings')
    inlines = [PlanPriceInline]


class MembershipAdmin(admin.ModelAdmin):
    list_display = ('get_email', 'first_name', 'last_name', 'end_date',
        'customer_id', 'cc_last4', 'remaining_job_postings',)
    search_fields = ('plan_type', 'coupon_code', 'first_name', 'last_name',
        'end_date', 'cc_last4', 'remaining_job_postings', 'email', 'address',
        'zip_code', 'city', 'state', 'country')
    fieldsets = (
        (None, {
            'fields': ('user', 'end_date', 'remaining_job_postings',)
        }),
        (strings.ADMIN_STRIPES_CUSTOMER_INFO, {
            'fields': ('customer_id', 'cc_last4',)
        }),
        (strings.ADMIN_PLAN_TYPE, {
            'fields': ('plan_type',)
        }),
        (strings.ADMIN_PURCHASE_INFO, {
            'fields': ('coupon_code',)
        }),
        (strings.ADMIN_CONTACT_INFO, {
            'fields': ('first_name', 'last_name', 'email',)
        }),
        (strings.ADMIN_BILLING_ADDRESS, {
            'fields': ('address', 'zip_code', 'city', 'state', 'country',)
        }),
    )


class CouponAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'discount')
    search_fields = ('code', 'discount', 'claimed_by__email')


admin.site.register(Plan, PlanAdmin)
admin.site.register(Membership, MembershipAdmin)
admin.site.register(Coupon, CouponAdmin)
