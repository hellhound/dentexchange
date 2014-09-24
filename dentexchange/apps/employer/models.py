# -*- coding:utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic

from libs.models.soft_deletable import (SoftDeletableModelManager,
    SoftDeletableModel)
from libs.models.indexable import IndexableModel
from libs import constants as lib_constants
from employee import constants as employee_constants
from matches.models import Match
from . import strings, constants


class Business(models.Model):
    user = models.OneToOneField(User, verbose_name=strings.BUSINESS_USER)
    number_offices = models.PositiveSmallIntegerField(
        verbose_name=strings.BUSINESS_NUMBER_OFFICES,
        choices=constants.BUSINESS_NUMBER_OFFICES_CHOICES)
    is_mso = models.BooleanField(verbose_name=strings.BUSINESS_IS_MSO,
        choices=lib_constants.YES_NO_CHOICES,
        default=lib_constants.YES_NO_CHOICES.YES)
    number_employees = models.PositiveSmallIntegerField(
        verbose_name=strings.BUSINESS_NUMBER_EMPLOYEES,
        choices=constants.BUSINESS_NUMBER_EMPLOYEES_CHOICES)

    class Meta(object):
        verbose_name = strings.BUSINESS_VERBOSE_NAME
        verbose_name_plural = strings.BUSINESS_VERBOSE_NAME_PLURAL

    def __unicode__(self):
        return self.user.email

    def get_email(self):
        return unicode(self)


class PraxisManager(SoftDeletableModelManager):
    pass


class Praxis(SoftDeletableModel):
    business = models.ForeignKey(Business,
        verbose_name=strings.PRAXIS_BUSINESS)
    ### Contact Info
    company_name = models.CharField(verbose_name=strings.PRAXIS_COMPANY_NAME,
        max_length=100)
    contact_first_name = models.CharField(
        verbose_name=strings.PRAXIS_CONTACT_FIRST_NAME, max_length=100)
    contact_last_name = models.CharField(
        verbose_name=strings.PRAXIS_CONTACT_LAST_NAME, max_length=100)
    ### Praxis Location
    address = models.CharField(verbose_name=strings.PRAXIS_ADDRESS,
        max_length=200)
    zip_code = models.DecimalField(verbose_name=strings.PRAXIS_ZIP_CODE,
        max_digits=5, decimal_places=0)
    city = models.CharField(verbose_name=strings.PRAXIS_CITY,
        max_length=100)
    state = models.CharField(verbose_name=strings.PRAXIS_STATE,
        choices=lib_constants.STATE_CHOICES, max_length=2)
    ### Type of Practice
    solo_practitioner = models.BooleanField(
        verbose_name=strings.PRAXIS_SOLO_PRACTITIONER)
    multi_practitioner = models.BooleanField(
        verbose_name=strings.PRAXIS_MULTI_PRACTITIONER)
    corporate = models.BooleanField(
        verbose_name=strings.PRAXIS_CORPORATE)
    ### Patients' Method of Payment
    fee_for_service = models.BooleanField(
        verbose_name=strings.PRAXIS_FEE_FOR_SERVICE)
    insurance = models.BooleanField(
        verbose_name=strings.PRAXIS_INSURANCE)
    capitation_medicaid = models.BooleanField(
        verbose_name=strings.PRAXIS_CAPITATION_MEDICAID)
    objects = PraxisManager()

    class Meta(object):
        verbose_name = strings.PRAXIS_VERBOSE_NAME
        verbose_name_plural = strings.PRAXIS_VERBOSE_NAME_PLURAL

    def __unicode__(self):
        return self.business.user.email

    def get_email(self):
        return unicode(self)


class JobPostingManager(SoftDeletableModelManager):
    pass


class JobPosting(SoftDeletableModel, IndexableModel):
    praxis = models.ForeignKey(Praxis,
        verbose_name=strings.JOB_POSTING_PRAXIS)
    ### General Info
    position_name = models.CharField(
        verbose_name=strings.JOB_POSTING_POSITION_NAME,
        max_length=100)
    posting_title = models.CharField(
        verbose_name=strings.JOB_POSTING_POSTING_TITLE,
        max_length=300)
    ### Job posting you are offering
    job_position = models.PositiveSmallIntegerField(
        verbose_name=strings.JOB_POSTING_JOB_POSITION,
        choices=employee_constants.JOB_POSITION_CHOICES)
    ### Type of schedule required
    schedule_type = models.BooleanField(
        verbose_name=strings.JOB_POSTING_SCHEDULE_TYPE,
        choices=employee_constants.SCHEDULE_TYPE_CHOICES,
        default=employee_constants.SCHEDULE_TYPE_CHOICES.PART_TIME)
    monday_daytime = models.BooleanField(
        verbose_name=strings.JOB_POSTING_MONDAY_DAYTIME, default=False)
    monday_evening = models.BooleanField(
        verbose_name=strings.JOB_POSTING_MONDAY_EVENING, default=False)
    tuesday_daytime = models.BooleanField(
        verbose_name=strings.JOB_POSTING_TUESDAY_DAYTIME, default=False)
    tuesday_evening = models.BooleanField(
        verbose_name=strings.JOB_POSTING_TUESDAY_EVENING, default=False)
    wednesday_daytime = models.BooleanField(
        verbose_name=strings.JOB_POSTING_WEDNESDAY_DAYTIME, default=False)
    wednesday_evening = models.BooleanField(
        verbose_name=strings.JOB_POSTING_WEDNESDAY_EVENING, default=False)
    thursday_daytime = models.BooleanField(
        verbose_name=strings.JOB_POSTING_THURSDAY_DAYTIME, default=False)
    thursday_evening = models.BooleanField(
        verbose_name=strings.JOB_POSTING_THURSDAY_EVENING, default=False)
    friday_daytime = models.BooleanField(
        verbose_name=strings.JOB_POSTING_FRIDAY_DAYTIME, default=False)
    friday_evening = models.BooleanField(
        verbose_name=strings.JOB_POSTING_FRIDAY_EVENING, default=False)
    saturday_daytime = models.BooleanField(
        verbose_name=strings.JOB_POSTING_SATURDAY_DAYTIME, default=False)
    saturday_evening = models.BooleanField(
        verbose_name=strings.JOB_POSTING_SATURDAY_EVENING, default=False)
    sunday_daytime = models.BooleanField(
        verbose_name=strings.JOB_POSTING_SUNDAY_DAYTIME, default=False)
    sunday_evening = models.BooleanField(
        verbose_name=strings.JOB_POSTING_SUNDAY_EVENING, default=False)
    ### Compensation
    compensation_type = models.BooleanField(
        verbose_name=strings.JOB_POSTING_COMPENSATION_TYPE,
        choices=employee_constants.COMPENSATION_TYPE_CHOICES,
        default=employee_constants.COMPENSATION_TYPE_CHOICES.HOURLY)
    hourly_wage = models.PositiveSmallIntegerField(
        verbose_name=strings.JOB_POSTING_HOURLY_WAGE,
        choices=employee_constants.HOURLY_WAGE_CHOICES,
        blank=True, null=True)
    annualy_wage = models.PositiveSmallIntegerField(
        verbose_name=strings.JOB_POSTING_ANNUALY_WAGE,
        choices=employee_constants.ANNUALY_WAGE_CHOICES,
        blank=True, null=True)
    production = models.BooleanField(
        verbose_name=strings.JOB_POSTING_PRODUCTION,
        default=False)
    collection = models.BooleanField(
        verbose_name=strings.JOB_POSTING_COLLECTION,
        default=False)
    ### Experience required
    experience_years = models.PositiveSmallIntegerField(
        verbose_name=strings.JOB_POSTING_EXPERIENCE_YEARS,
        choices=employee_constants.EXPERIENCE_YEARS_CHOICES)
    ### Benefits being offered
    benefit_1 = models.BooleanField(
        verbose_name=strings.JOB_POSTING_BENEFIT_1, default=False)
    benefit_2 = models.BooleanField(
        verbose_name=strings.JOB_POSTING_BENEFIT_2, default=False)
    benefit_3 = models.BooleanField(
        verbose_name=strings.JOB_POSTING_BENEFIT_3, default=False)
    benefit_4 = models.BooleanField(
        verbose_name=strings.JOB_POSTING_BENEFIT_4, default=False)
    benefit_5 = models.BooleanField(
        verbose_name=strings.JOB_POSTING_BENEFIT_5, default=False)
    benefit_6 = models.BooleanField(
        verbose_name=strings.JOB_POSTING_BENEFIT_6, default=False)
    benefit_other = models.BooleanField(
        verbose_name=strings.JOB_POSTING_BENEFIT_OTHER, default=False)
    benefit_other_text = models.TextField(
        verbose_name=strings.JOB_POSTING_BENEFIT_OTHER,
        blank=True)
    ### Visa
    visa = models.BooleanField(
        verbose_name=strings.JOB_POSTING_VISA,
        choices=lib_constants.YES_NO_CHOICES,
        default=lib_constants.YES_NO_CHOICES.YES)
    ### Additional Comments
    additional_comments = models.TextField(
        verbose_name=strings.JOB_POSTING_ADDITIONAL_COMMENTS,
        blank=True)
    is_posted = models.BooleanField(
        verbose_name=strings.JOB_POSTING_IS_POSTED, default=False)
    matches = generic.GenericRelation(Match,
        content_type_field='match_content_type',
        object_id_field='match_object_id')
    objects = JobPostingManager()

    class Meta(object):
        verbose_name = strings.JOB_POSTING_VERBOSE_NAME
        verbose_name_plural = strings.JOB_POSTING_VERBOSE_NAME_PLURAL

    def __unicode__(self):
        return self.position_name
