# -*- coding:utf-8 -*-
import hashlib
from uuid import uuid4

from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.utils.translation import ngettext as _n

from iso3166 import countries

from tinymce.models import HTMLField

from . import strings, constants


class Plan(models.Model):
    title = models.CharField(verbose_name=strings.PLAN_TITLE,
        max_length=50)
    for_employer = models.BooleanField(
        verbose_name=strings.PLAN_FOR_EMPLOYER,
        choices=constants.FOR_EMPLOYER_CHOICES,
        default=constants.FOR_EMPLOYER_CHOICES.EMPLOYER)
    content_description = HTMLField(
        verbose_name=strings.PLAN_CONTENT_DESCRIPTION,
        help_text=strings.PLAN_CONTENT_DESCRIPTION_HELP_TEXT)

    class Meta(object):
        verbose_name = strings.PLAN_VERBOSE_NAME
        verbose_name_plural = strings.PLAN_VERBOSE_NAME_PLURAL
        ordering = ['pk']

    def __unicode__(self):
        return self.title


class PlanPrice(models.Model):
    plan = models.ForeignKey(Plan, verbose_name=strings.PLAN_PRICE_PLAN)
    price = models.DecimalField(verbose_name=strings.PLAN_PRICE_PRICE,
        max_digits=9, decimal_places=2, default=0)
    tag = models.CharField(verbose_name=strings.PLAN_PRICE_TAG,
        max_length=50, blank=True)
    is_free = models.BooleanField(verbose_name=strings.PLAN_PRICE_IS_FREE,
        default=False)
    duration_magnitude = models.PositiveIntegerField(
        verbose_name=strings.PLAN_PRICE_DURATION_MAGNITUDE,
        default=0)
    duration_unit = models.PositiveSmallIntegerField(
        verbose_name=strings.PLAN_PRICE_DURATION_UNIT,
        choices=constants.DURATION_UNIT_CHOICES)
    total_allowed_job_postings = models.PositiveIntegerField(
        verbose_name=strings.PLAN_PRICE_TOTAL_ALLOWED_JOB_POSTINGS,
        default=1)

    class Meta(object):
        verbose_name = strings.PLAN_PRICE_VERBOSE_NAME
        verbose_name_plural = strings.PLAN_PRICE_VERBOSE_NAME_PLURAL

    def __unicode__(self):
        return unicode(self.title)

    @property
    def title(self):
        if self.is_free:
            return strings.PLAN_PRICE_TITLE_FREE
        elif self.duration_unit == constants.DURATION_UNIT_CHOICES.MONTHS:
            singular = strings.PLAN_PRICE_TITLE_MONTH
            plural = strings.PLAN_PRICE_TITLE_MONTH_PLURAL
        else:
            singular = strings.PLAN_PRICE_TITLE_YEAR
            plural = strings.PLAN_PRICE_TITLE_YEAR_PLURAL
        return '%i %s' % (
            self.duration_magnitude,
            _n(singular, plural, self.duration_magnitude))


class Membership(models.Model):
    user = models.OneToOneField(User, verbose_name=strings.MEMBERSHIP_USER)
    # Stripe's customer id
    customer_id = models.CharField(
        verbose_name=strings.MEMBERSHIP_STRIPES_CUSTOMER_ID,
        max_length=100, blank=True, null=True)
    cc_last4 = models.PositiveIntegerField(
        verbose_name=strings.MEMBERSHIP_STRIPES_CC_LAST4,
        null=True)
    # Plan type
    plan_type = models.ForeignKey(PlanPrice,
        verbose_name=strings.MEMBERSHIP_PLAN_TYPE)
    # Purchase Information
    coupon_code = models.ForeignKey('Coupon',
        verbose_name=strings.MEMBERSHIP_COUPON_CODE,
        blank=True, null=True)
    # Contact Information
    first_name = models.CharField(
        verbose_name=strings.MEMBERSHIP_FIRST_NAME,
        max_length=100)
    last_name = models.CharField(
        verbose_name=strings.MEMBERSHIP_LAST_NAME,
        max_length=100)
    email = models.EmailField(
        verbose_name=strings.MEMBERSHIP_EMAIL)
    # Billing Address
    address = models.CharField(
        verbose_name=strings.MEMBERSHIP_ADDRESS,
        max_length=200)
    zip_code = models.DecimalField(
        verbose_name=strings.MEMBERSHIP_ZIP_CODE,
        max_digits=5, decimal_places=0)
    city = models.CharField(
        verbose_name=strings.MEMBERSHIP_CITY,
        max_length=100)
    state = models.CharField(
        verbose_name=strings.MEMBERSHIP_STATE,
        max_length=100)
    country = models.CharField(
        verbose_name=strings.MEMBERSHIP_COUNTRY,
        choices=[(c.alpha2, c.name) for c in countries],
        max_length=2)
    end_date = models.DateTimeField(
        verbose_name=strings.MEMBERSHIP_END_DATE,
        null=True)
    remaining_job_postings = models.PositiveIntegerField(
        verbose_name=strings.MEMBERSHIP_AVAILABLE_JOB_POSTINGS,
        blank=True, default=0)

    class Meta(object):
        verbose_name = strings.MEMBERSHIP_VERBOSE_NAME
        verbose_name_plural = strings.MEMBERSHIP_VERBOSE_NAME_PLURAL

    def __unicode__(self):
        return u'%s %s' % (self.first_name, self.last_name)

    def get_email(self):
        return self.user.email


class CouponManager(models.Manager):
    def is_valid(self, coupon_code):
        if coupon_code is None or coupon_code.strip() == '':
            return False
        return self.get_queryset().filter(
            code=coupon_code, claimed_by__isnull=True).count() > 0

    def get_discount(self, coupon_code):
        return self.get_queryset().get(code=coupon_code).discount


class Coupon(models.Model):
    code = models.CharField(
        verbose_name=strings.COUPON_CODE,
        max_length=10, blank=True, editable=False, unique=True)
    discount = models.DecimalField(
        verbose_name=strings.COUPON_DISCOUNT,
        max_digits=9, decimal_places=2)
    claimed_by = models.OneToOneField(User, verbose_name=strings.COUPON_USER,
        blank=True, null=True, editable=False)
    objects = CouponManager()

    class Meta(object):
        verbose_name = strings.COUPON_VERBOSE_NAME
        verbose_name_plural = strings.COUPON_VERBOSE_NAME_PLURAL

    def __unicode__(self):
        try:
            return strings.COUPON_CLAIMED_UNICODE % (self.code, self.claimed_by)
        except Membership.DoesNotExist:
            return strings.COUPON_UNCLAIMED_UNICODE % self.code

    def get_email(self):
        return self.claimed_by.email

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.code = hashlib.sha512(
                unicode(uuid4())).hexdigest()[:10].upper()
        super(Coupon, self).save(*args, **kwargs)
