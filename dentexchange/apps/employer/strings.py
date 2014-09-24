# -*- coding:utf-8 -*-
from django.utils.translation import ugettext_lazy as _

# Business' strings

BUSINESS_USER = _(u'User')
BUSINESS_NUMBER_OFFICES = _(u'Number of Offices')
BUSINESS_IS_MSO = _(u'Is a MSO (Dental Franchise)?')
BUSINESS_NUMBER_EMPLOYEES = _(u'Number of Employees')
BUSINESS_VERBOSE_NAME = _(u'Business')
BUSINESS_VERBOSE_NAME_PLURAL = _(u'Businesses')
### Personal Info
BUSINESS_FIRST_NAME = _(u'First Name')
BUSINESS_LAST_NAME = _(u'Last Name')
BUSINESS_PERSONAL_ADDRESS = _(u'Street')
BUSINESS_ZIP_CODE = _(u'Zip Code')
BUSINESS_CITY = _(u'City')
BUSINESS_STATE = _(u'State')

# Praxis' strings

PRAXIS_BUSINESS = _(u'Business')
### Contact Info
PRAXIS_COMPANY_NAME = _(u'Practice Name')
PRAXIS_CONTACT_FIRST_NAME = _(u'Practice Contact First Name')
PRAXIS_CONTACT_LAST_NAME = _(u'Practice Contact Last Name')
### Praxis Location
PRAXIS_ADDRESS = _(u'Street')
PRAXIS_ZIP_CODE = _(u'Zip Code')
PRAXIS_CITY = _(u'City')
PRAXIS_STATE = _(u'State')
### Type of Practice
PRAXIS_SOLO_PRACTITIONER = _(u'Solo Practitioner')
PRAXIS_MULTI_PRACTITIONER = _(u'Multi-Practitioner')
PRAXIS_CORPORATE = _(u'Corporate')
### Patients' Method of Payment
PRAXIS_FEE_FOR_SERVICE = _(u'Fee for Service')
PRAXIS_INSURANCE = _(u'Insurance')
PRAXIS_CAPITATION_MEDICAID = _(u'Capitation/Medicaid')
PRAXIS_VERBOSE_NAME = _(u'Practice')
PRAXIS_VERBOSE_NAME_PLURAL = _(u'Practices')

# JobPosting's strings

JOB_POSTING_USER = _(u'User')
JOB_POSTING_PRAXIS = _(u'Practice')
### General Info
JOB_POSTING_POSITION_NAME = _(
    u'Position Name for internal reference')
JOB_POSTING_POSTING_TITLE = _(
    u'Posting Title as employees will see it')
### Job Posting you are offering
JOB_POSTING_JOB_POSITION = _(u'Job Position Offered')
### Type of schedule required
JOB_POSTING_SCHEDULE_TYPE = _(u'Type of Schedule Required')
JOB_POSTING_MONDAY_DAYTIME = _(u'Monday Daytime')
JOB_POSTING_MONDAY_EVENING = _(u'Monday Evening')
JOB_POSTING_TUESDAY_DAYTIME = _(u'Tuesday Daytime')
JOB_POSTING_TUESDAY_EVENING = _(u'Tuesday Evening')
JOB_POSTING_WEDNESDAY_DAYTIME = _(u'Wednesday Daytime')
JOB_POSTING_WEDNESDAY_EVENING = _(u'Wednesday Evening')
JOB_POSTING_THURSDAY_DAYTIME = _(u'Thursday Daytime')
JOB_POSTING_THURSDAY_EVENING = _(u'Thursday Evening')
JOB_POSTING_FRIDAY_DAYTIME = _(u'Friday Daytime')
JOB_POSTING_FRIDAY_EVENING = _(u'Friday Evening')
JOB_POSTING_SATURDAY_DAYTIME = _(u'Saturday Daytime')
JOB_POSTING_SATURDAY_EVENING = _(u'Saturday Evening')
JOB_POSTING_SUNDAY_DAYTIME = _(u'Sunday Daytime')
JOB_POSTING_SUNDAY_EVENING = _(u'Sunday Evening')
### Compensation
JOB_POSTING_COMPENSATION_TYPE = _(u'Compensation')
JOB_POSTING_HOURLY_WAGE = _(u'Hourly Wage')
JOB_POSTING_ANNUALY_WAGE = _(u'Annualy Wage')
JOB_POSTING_PRODUCTION = _(u'Production')
JOB_POSTING_COLLECTION = _(u'Colleciton')
### Experience required
JOB_POSTING_EXPERIENCE_YEARS = _(u'Years of Experience')
### Benefits being offered
JOB_POSTING_BENEFIT_1 = _(u'Health Insurance')
JOB_POSTING_BENEFIT_2 = _(u'Dental Insurance')
JOB_POSTING_BENEFIT_3 = _(u'401K/Retirement Planning')
JOB_POSTING_BENEFIT_4 = _(u'Malpractice Insurance')
JOB_POSTING_BENEFIT_5 = _(u'Disability Insurance')
JOB_POSTING_BENEFIT_6 = _(
    u'Registration Fee for Continuing Education Courses')
JOB_POSTING_BENEFIT_OTHER = _(u'Other')
JOB_POSTING_BENEFIT_OTHER_TEXT = _(u'Please specify other benefits')
### Visa
JOB_POSTING_VISA = _(u'Can you sponsor a visa?')
### Additional Comments / Requirements
JOB_POSTING_ADDITIONAL_COMMENTS = _(
    u'Please list additional Comments / Requirements')
JOB_POSTING_IS_POSTED = _(u'Is Posted?')
JOB_POSTING_VERBOSE_NAME = _(u'Job Posting')
JOB_POSTING_VERBOSE_NAME_PLURAL = _(u'Job Postings')

# JobPostingForm's errors
JOB_POSTING_FORM_INCOMPLETE_FORM_ERROR = _(u'You have not filled out all ' \
    u'the fields yet.')

BUSINESS_NUMBER_OFFICES_10_PLUS_CHOICE = _(u'10+')
BUSINESS_NUMBER_EMPLOYEES_10_PLUS_CHOICE = _(u'10+')

# BusinessForm Errors
BUSINESS_FORM_INCOMPLETE_FORM_ERROR = _(u'You have not filled out all ' \
    u'the fields yet.')

# AddNewPostingFormView's messages
ADD_NEW_POSTING_FORM_VIEW_LIMIT_EXCEEDED = _(u'You\'ve exceeded the job ' \
    u'posting limit for your current plan.')

# Admin strings
ADMIN_CONTACT_INFO = _(u'Contact Info')
ADMIN_PRAXIS_LOCATION = _(u'Practice Location')
ADMIN_PRACTICE_TYPE = _(u'Type of Practice')
ADMIN_PATIENTS_PAYMENT_METHOD = _(u'Patients\' Method of Payment')
ADMIN_GENERAL_INFO = _(u'General Info')
ADMIN_JOB_POSTING_OFFERED = _(u'Job posting you are offering')
ADMIN_SCHEDULE_TYPE = _(u'Type of schedule required')
ADMIN_COMPENSATION = _(u'Compensation')
ADMIN_EXPERIENCE_REQUIRED = _(u'Experience required')
ADMIN_BENEFITS_BEING_OFFERED = _(u'Benefits being offered')
ADMIN_ADDITIONAL_COMMENTS = _(u'Additional Comments')

# Employer's contact message subject
EMPLOYER_CONTACT_SUBJECT = _(u'Looking for hire')
