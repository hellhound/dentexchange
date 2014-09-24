# -*- coding:utf-8 -*-
from django.utils.translation import ugettext_lazy as _

# Plan fields' labels
PLAN_TITLE = _(u'Title')
PLAN_FOR_EMPLOYER = _(u'Is this plan for employers?')
PLAN_CONTENT_DESCRIPTION = _(u'Content Description')
PLAN_CONTENT_DESCRIPTION_HELP_TEXT = _(
    u'Use bullets to denote each feature the plan offers')
PLAN_VERBOSE_NAME = _(u'Plan')
PLAN_VERBOSE_NAME_PLURAL = _(u'Plans')

# PlanPrice fields's labels
PLAN_PRICE_PLAN = _(u'Price')
PLAN_PRICE_TITLE = _(u'Title')
PLAN_PRICE_PRICE = _(u'Price')
PLAN_PRICE_TAG = _(u'Tag')
PLAN_PRICE_IS_FREE = _(u'Is Free?')
PLAN_PRICE_DURATION_MAGNITUDE = _(u'Duration')
PLAN_PRICE_DURATION_UNIT = _(u'Unit')
PLAN_PRICE_TOTAL_ALLOWED_JOB_POSTINGS = _(u'Number of job postings allowed')
PLAN_PRICE_VERBOSE_NAME = _(u'Plan price')
PLAN_PRICE_VERBOSE_NAME_PLURAL = _(u'Plan prices')

# PlanPrice.duration_unit choices
DURATION_UNIT_CHOICES_UNLIMITED = _(u'Unlimited')
DURATION_UNIT_CHOICES_MONTHS = _(u'Months')
DURATION_UNIT_CHOICES_YEARS = _(u'Years')

# PlanPrice's titles
PLAN_PRICE_TITLE_FREE = _(u'Free')
PLAN_PRICE_TITLE_MONTH = u'Month'
PLAN_PRICE_TITLE_MONTH_PLURAL = u'Months'
PLAN_PRICE_TITLE_YEAR = u'Year'
PLAN_PRICE_TITLE_YEAR_PLURAL = u'Years'

# Membership fields' labels
MEMBERSHIP_USER = _(u'User')
# Stripe's fields
MEMBERSHIP_STRIPES_CUSTOMER_ID = _(u'Stripe\'s customer id')
MEMBERSHIP_STRIPES_CC_LAST4 = _(u'Last 4 CC digits')
# Plan type
MEMBERSHIP_PLAN_TYPE = _(u'Plan Type')
# Purchase Information
MEMBERSHIP_COUPON_CODE = _(u'Coupon Code')
# Contact Information
MEMBERSHIP_FIRST_NAME = _(u'First Name')
MEMBERSHIP_LAST_NAME = _(u'Last Name')
MEMBERSHIP_EMAIL = _(u'Email Address')
# Billing Info
MEMBERSHIP_CREDIT_CARD = _(u'Credit Card Number')
MEMBERSHIP_CVV = _(u'CVV')
MEMBERSHIP_EXPIRY_MONTH = _(u'Expiry Month')
MEMBERSHIP_EXPIRY_YEAR = _(u'Expiry Year')
# Billing Address
MEMBERSHIP_ADDRESS = _(u'Street')
MEMBERSHIP_ZIP_CODE = _(u'Zip Code')
MEMBERSHIP_CITY = _(u'City')
MEMBERSHIP_STATE = _(u'State')
MEMBERSHIP_COUNTRY = _(u'Country')
MEMBERSHIP_END_DATE = _(u'Plan\'s ending date')
MEMBERSHIP_AVAILABLE_JOB_POSTINGS = _(u'Remaining job postings')
MEMBERSHIP_VERBOSE_NAME = _(u'Membership')
MEMBERSHIP_VERBOSE_NAME_PLURAL = _(u'Memberships')

# Membership.expiry_moth choices
EXPIRY_MONTH_CHOICES_1 = _(u'01 - January')
EXPIRY_MONTH_CHOICES_2 = _(u'02 - February')
EXPIRY_MONTH_CHOICES_3 = _(u'03 - March')
EXPIRY_MONTH_CHOICES_4 = _(u'04 - April')
EXPIRY_MONTH_CHOICES_5 = _(u'05 - May')
EXPIRY_MONTH_CHOICES_6 = _(u'06 - June')
EXPIRY_MONTH_CHOICES_7 = _(u'07 - July')
EXPIRY_MONTH_CHOICES_8 = _(u'08 - August')
EXPIRY_MONTH_CHOICES_9 = _(u'09 - September')
EXPIRY_MONTH_CHOICES_10 = _(u'10 - October')
EXPIRY_MONTH_CHOICES_11 = _(u'11 - November')
EXPIRY_MONTH_CHOICES_12 = _(u'12 - December')

# Coupon fields' labels
COUPON_USER = _(u'Claimed By')
COUPON_CODE = _(u'Auto-Generated Code')
COUPON_DISCOUNT = _(u'Discount')
COUPON_VERBOSE_NAME = _(u'Coupon')
COUPON_VERBOSE_NAME_PLURAL = (u'Coupons')
COUPON_CLAIMED_UNICODE = _(u'Code: %s - Claimed by: %s')
COUPON_UNCLAIMED_UNICODE = _(u'Code: %s - Unclaimed')

# MembershipForm's errors
MEMBERSHIP_FORM_INVALID_COUPON_ERROR = (
    u'This coupon has already been claimed or is invalid')

# Admin strings
ADMIN_STRIPES_CUSTOMER_INFO = (u'Stripe\'s customer info')
ADMIN_PLAN_TYPE = _(u'Plan Type')
ADMIN_PURCHASE_INFO = _(u'Purchase Information')
ADMIN_CONTACT_INFO = _(u'Contact Information')
ADMIN_BILLING_INFO = _(u'Billing Info')
ADMIN_BILLING_ADDRESS = _(u'Billing Address')
