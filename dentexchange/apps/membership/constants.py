# -*- coding:utf-8 -*-
from django.utils.translation import ugettext_lazy as _

from libs.choices import Enumeration
from . import strings

# Plan's constants
FOR_EMPLOYER_CHOICES = Enumeration([
    (True, 'EMPLOYER', _(u'Yes')),
    (False, 'EMPLOYEE', _(u'No')),
])

# PlanPrice's constants
DURATION_UNIT_CHOICES = Enumeration([
    (0, 'UNLIMITED', strings.DURATION_UNIT_CHOICES_UNLIMITED),
    (1, 'MONTHS', strings.DURATION_UNIT_CHOICES_MONTHS),
    (2, 'YEARS', strings.DURATION_UNIT_CHOICES_YEARS),
])

# Membership's constants
EXPIRY_MONTH_CHOICES = Enumeration([
    (1, 'MONTH_1', strings.EXPIRY_MONTH_CHOICES_1),
    (2, 'MONTH_2', strings.EXPIRY_MONTH_CHOICES_2),
    (3, 'MONTH_3', strings.EXPIRY_MONTH_CHOICES_3),
    (4, 'MONTH_4', strings.EXPIRY_MONTH_CHOICES_4),
    (5, 'MONTH_5', strings.EXPIRY_MONTH_CHOICES_5),
    (6, 'MONTH_6', strings.EXPIRY_MONTH_CHOICES_6),
    (7, 'MONTH_7', strings.EXPIRY_MONTH_CHOICES_7),
    (8, 'MONTH_8', strings.EXPIRY_MONTH_CHOICES_8),
    (9, 'MONTH_9', strings.EXPIRY_MONTH_CHOICES_9),
    (10, 'MONTH_10', strings.EXPIRY_MONTH_CHOICES_10),
    (11, 'MONTH_11', strings.EXPIRY_MONTH_CHOICES_11),
    (12, 'MONTH_12', strings.EXPIRY_MONTH_CHOICES_12),
])

STRIPE_TO_FORM_FIELDS_MAPPING = {
    'number': 'credit_card',
    'cvc': 'cvv',
    'exp-month': 'expiry_month',
    'exp-year': 'expiry_year',
}
