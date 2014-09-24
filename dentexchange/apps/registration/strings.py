# -*- coding:utf-8 -*-
from django.utils.translation import ugettext_lazy as _


### User Registration
USER_REGISTRATION_USER = _(u'User')
USER_REGISTRATION_EMAIL = _(u'Email')
USER_REGISTRATION_ACCOUNT_TYPE = _(u'Account type')
USER_REGISTRATION_PASSWORD = _(u'Password')
USER_REGISTRATION_CONFIRM_PASSWORD = _(u'Confirm password')
### Personal Info
USER_REGISTRATION_FIRST_NAME = _(u'First Name')
USER_REGISTRATION_LAST_NAME = _(u'Last Name')
USER_REGISTRATION_PERSONAL_ADDRESS = _(u'Street')
USER_REGISTRATION_ZIP_CODE = _(u'Zip Code')
USER_REGISTRATION_CITY = _(u'City')
USER_REGISTRATION_STATE = _(u'State')
USER_REGISTRATION_VERBOSE_NAME = _(u'User registration')
USER_REGISTRATION_VERBOSE_NAME_PLURAL = _(u'User registrations')
USER_REGISTRATION_TERMS_OF_USE = _(u'I agree with the Terms of Use')

# UserRegistration.is_employer choices
IS_EMPLOYER_CHOICES_EMPLOYER = _(u'I\'m an employer')
IS_EMPLOYER_CHOICES_EMPLOYEE = _(u'I\'m an employee')

#RegistrationForm errors
REGISTRATION_FORM_PASSWORD_ISNT_VALID = _(u'Please enter the same password '
    u'in \'Confirm Password\'.')
REGISTRATION_FORM_EMAIL_ALREADY_TAKEN = _(u'The email is already taken.')
REGISTRATION_FORM_USERNAME_COLLISION = _(u'Please use another email.')
REGISTRATION_FORM_TERMS_OF_USE_ERROR = _(
    u'You should agree with the Terms of Use.')

# send_welcome_message's strings
SEND_WELCOME_MESSAGE = _(u'Welcome to Dentexchange!')

# Admin strings

ADMIN_PERSONAL_INFO = _(u'Personal Info')
