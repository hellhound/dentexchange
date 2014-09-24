# -*- coding:utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic

from validatedfile.fields import ValidatedFileField

from libs import constants as lib_constants
from libs.models.indexable import IndexableModel
from matches.models import Match
from . import strings, constants


class EmployeeQuestionnaire(IndexableModel):
    user = models.OneToOneField(User,
        verbose_name=strings.EMPLOYEE_QUESTIONNAIRE_USER)
    ### Job Position you're looking for
    job_position = models.PositiveSmallIntegerField(
        verbose_name=strings.EMPLOYEE_QUESTIONNAIRE_JOB_POSITION,
        choices=constants.JOB_POSITION_CHOICES,
        blank=True, null=True)
    ### Type of Practice
    solo_practitioner = models.BooleanField(
        verbose_name=strings.EMPLOYEE_QUESTIONNAIRE_SOLO_PRACTITIONER)
    multi_practitioner = models.BooleanField(
        verbose_name=strings.EMPLOYEE_QUESTIONNAIRE_MULTI_PRACTITIONER)
    corporate = models.BooleanField(
        verbose_name=strings.EMPLOYEE_QUESTIONNAIRE_CORPORATE)
    ### Patients' Method of Payment
    fee_for_service = models.BooleanField(
        verbose_name=strings.EMPLOYEE_QUESTIONNAIRE_FEE_FOR_SERVICE)
    insurance = models.BooleanField(
        verbose_name=strings.EMPLOYEE_QUESTIONNAIRE_INSURANCE)
    capitation_medicaid = models.BooleanField(
        verbose_name=strings.EMPLOYEE_QUESTIONNAIRE_CAPITATION_MEDICAID)
    ### Location
    zip_code = models.DecimalField(
        verbose_name=strings.EMPLOYEE_QUESTIONNAIRE_ZIP_CODE,
        max_digits=5, decimal_places=0,
        blank=True, null=True)
    city = models.CharField(
        verbose_name=strings.EMPLOYEE_QUESTIONNAIRE_CITY,
        max_length=100, blank=True)
    state = models.CharField(
        verbose_name=strings.EMPLOYEE_QUESTIONNAIRE_STATE,
        choices=lib_constants.STATE_CHOICES,
        max_length=2, blank=True)
    distance = models.PositiveSmallIntegerField(
        verbose_name=strings.EMPLOYEE_QUESTIONNAIRE_DISTANCE,
        choices=constants.DISTANCE_CHOICES,
        blank=True, null=True)
    ### Type of schedule required
    schedule_type = models.BooleanField(
        verbose_name=strings.EMPLOYEE_QUESTIONNAIRE_SCHEDULE_TYPE,
        choices=constants.SCHEDULE_TYPE_CHOICES,
        default=constants.SCHEDULE_TYPE_CHOICES.PART_TIME)
    monday_daytime = models.BooleanField(
        verbose_name=strings.EMPLOYEE_QUESTIONNAIRE_MONDAY_DAYTIME,
        default=False)
    monday_evening = models.BooleanField(
        verbose_name=strings.EMPLOYEE_QUESTIONNAIRE_MONDAY_EVENING,
        default=False)
    tuesday_daytime = models.BooleanField(
        verbose_name=strings.EMPLOYEE_QUESTIONNAIRE_TUESDAY_DAYTIME,
        default=False)
    tuesday_evening = models.BooleanField(
        verbose_name=strings.EMPLOYEE_QUESTIONNAIRE_TUESDAY_EVENING,
        default=False)
    wednesday_daytime = models.BooleanField(
        verbose_name=strings.EMPLOYEE_QUESTIONNAIRE_WEDNESDAY_DAYTIME,
        default=False)
    wednesday_evening = models.BooleanField(
        verbose_name=strings.EMPLOYEE_QUESTIONNAIRE_WEDNESDAY_EVENING,
        default=False)
    thursday_daytime = models.BooleanField(
        verbose_name=strings.EMPLOYEE_QUESTIONNAIRE_THURSDAY_DAYTIME,
        default=False)
    thursday_evening = models.BooleanField(
        verbose_name=strings.EMPLOYEE_QUESTIONNAIRE_THURSDAY_EVENING,
        default=False)
    friday_daytime = models.BooleanField(
        verbose_name=strings.EMPLOYEE_QUESTIONNAIRE_FRIDAY_DAYTIME,
        default=False)
    friday_evening = models.BooleanField(
        verbose_name=strings.EMPLOYEE_QUESTIONNAIRE_FRIDAY_EVENING,
        default=False)
    saturday_daytime = models.BooleanField(
        verbose_name=strings.EMPLOYEE_QUESTIONNAIRE_SATURDAY_DAYTIME,
        default=False)
    saturday_evening = models.BooleanField(
        verbose_name=strings.EMPLOYEE_QUESTIONNAIRE_SATURDAY_EVENING,
        default=False)
    sunday_daytime = models.BooleanField(
        verbose_name=strings.EMPLOYEE_QUESTIONNAIRE_SUNDAY_DAYTIME,
        default=False)
    sunday_evening = models.BooleanField(
        verbose_name=strings.EMPLOYEE_QUESTIONNAIRE_SUNDAY_EVENING,
        default=False)
    ### Compensation
    compensation_type = models.BooleanField(
        verbose_name=strings.EMPLOYEE_QUESTIONNAIRE_COMPENSATION_TYPE,
        choices=constants.COMPENSATION_TYPE_CHOICES,
        default=constants.COMPENSATION_TYPE_CHOICES.HOURLY)
    hourly_wage = models.PositiveSmallIntegerField(
        verbose_name=strings.EMPLOYEE_QUESTIONNAIRE_HOURLY_WAGE,
        choices=constants.HOURLY_WAGE_CHOICES,
        blank=True, null=True)
    annualy_wage = models.PositiveSmallIntegerField(
        verbose_name=strings.EMPLOYEE_QUESTIONNAIRE_ANNUALY_WAGE,
        choices=constants.ANNUALY_WAGE_CHOICES,
        blank=True, null=True)
    production = models.BooleanField(
        verbose_name=strings.EMPLOYEE_QUESTIONNAIRE_PRODUCTION,
        default=False)
    collection = models.BooleanField(
        verbose_name=strings.EMPLOYEE_QUESTIONNAIRE_COLLECTION,
        default=False)
    ### Experience
    experience_years = models.PositiveSmallIntegerField(
        verbose_name=strings.EMPLOYEE_QUESTIONNAIRE_EXPERIENCE_YEARS,
        choices=constants.EXPERIENCE_YEARS_CHOICES,
        blank=True, null=True)
    ### Education
    dental_school = models.CharField(
        verbose_name=strings.EMPLOYEE_QUESTIONNAIRE_DENTAL_SCHOOL,
        max_length=200, blank=True)
    graduation_year = models.PositiveSmallIntegerField(
        verbose_name=strings.EMPLOYEE_QUESTIONNAIRE_GRADUATION_YEAR,
        choices=constants.GRADUATION_YEAR_CHOICES,
        blank=True, null=True)
    ### Visa
    visa = models.BooleanField(
        verbose_name=strings.EMPLOYEE_QUESTIONNAIRE_VISA,
        choices=lib_constants.YES_NO_CHOICES,
        default=lib_constants.YES_NO_CHOICES.YES)
    ### Specific strengths
    specific_strengths = models.TextField(
        verbose_name=strings.EMPLOYEE_QUESTIONNAIRE_SPECIFIC_STRENGTHS,
        blank=True)
    ### Visibility
    is_private = models.BooleanField(
        verbose_name=strings.EMPLOYEE_QUESTIONNAIRE_IS_PRIVATE,
        help_text=strings.EMPLOYEE_QUESTIONNAIRE_IS_PRIVATE_HELP_TEXT,
        default=False)
    matches = generic.GenericRelation(Match,
        content_type_field='match_content_type',
        object_id_field='match_object_id')

    class Meta(object):
        verbose_name = strings.EMPLOYEE_QUESTIONNAIRE_VERBOSE_NAME
        verbose_name_plural = strings.EMPLOYEE_QUESTIONNAIRE_VERBOSE_NAME_PLURAL

    def __unicode__(self):
        return self.user.email

    def get_email(self):
        return unicode(self)

    def get_location(self):
        return 


class Resume(models.Model):
    user = models.OneToOneField(User, verbose_name=strings.RESUME_USER)
    cv_file = ValidatedFileField(upload_to='employee/resumes',
        verbose_name=strings.RESUME_CV_FILE,
        help_text=strings.RESUME_CV_FILE_HELP_TEXT,
        max_upload_size=constants.RESUME_CV_FILE_MAX_UPLOAD_SIZE,
        content_types=constants.RESUME_CV_FILE_CONTENT_TYPES,
        null=True, blank=True)

    class Meta(object):
        verbose_name = strings.RESUME_VERBOSE_NAME
        verbose_name_plural = strings.RESUME_VERBOSE_NAME_PLURAL

    def __unicode__(self):
        return self.user.email

    def get_email(self):
        return unicode(self)
