# -*- coding:utf-8 -*-
from libs.choices import Enumeration
from . import strings

BUSINESS_NUMBER_OFFICES_CHOICES = Enumeration([
    (1, 'CHOICE_1', unicode(1)),
    (2, 'CHOICE_2', unicode(2)),
    (3, 'CHOICE_3', unicode(3)),
    (4, 'CHOICE_4', unicode(4)),
    (5, 'CHOICE_5', unicode(5)),
    (6, 'CHOICE_6', unicode(6)),
    (7, 'CHOICE_7', unicode(7)),
    (8, 'CHOICE_8', unicode(8)),
    (9, 'CHOICE_9', unicode(9)),
    (10, 'CHOICE_10', unicode(10)),
    (11, 'CHOICE_11', strings.BUSINESS_NUMBER_OFFICES_10_PLUS_CHOICE),
])

BUSINESS_NUMBER_EMPLOYEES_CHOICES = Enumeration([
    (1, 'CHOICE_1', unicode(1)),
    (2, 'CHOICE_2', unicode(2)),
    (3, 'CHOICE_3', unicode(3)),
    (4, 'CHOICE_4', unicode(4)),
    (5, 'CHOICE_5', unicode(5)),
    (6, 'CHOICE_6', unicode(6)),
    (7, 'CHOICE_7', unicode(7)),
    (8, 'CHOICE_8', unicode(8)),
    (9, 'CHOICE_9', unicode(9)),
    (10, 'CHOICE_10', unicode(10)),
    (11, 'CHOICE_11', strings.BUSINESS_NUMBER_EMPLOYEES_10_PLUS_CHOICE),
])

# JobPostingForm's error codes
JOB_POSTING_FORM_INCOMPLETE_FORM_ERROR_CODE = 1000

# BusinessForm error codes
BUSINESS_FORM_INCOMPLETE_FORM_ERROR_CODE = 1000
