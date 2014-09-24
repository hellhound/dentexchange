# -*- coding:utf-8 -*-
from django.utils.translation import ugettext_lazy as _

# RecoveryToken's strings
RECOVERY_TOKEN_USER = _(u'User')
RECOVERY_TOKEN_TIMESTAMP = _(u'Timestamp')
RECOVERY_TOKEN_TOKEN = _(u'Token')

# ResetForm's strings
RESET_FORM_EMAIL = _(u'Email')
RESET_FORM_EMAIL_HELP_TEXT = _(u'Please provide you account\'s email address')
RESET_FORM_EMAIL_DOESNT_EXIST = _(
    u'We couldn\'t find a Dentexchange account associated with %s')

# EditPasswordForm's strings
EDIT_PASSWORD_FORM_CONFIRM_PASSWORD = _(u'Confirm password')

# EditPasswordForm's errors
EDIT_PASSWORD_FORM_PASSWORD_ISNT_VALID = _(u'Please enter the same password '
    u'in \'Confirm Password\'.')

# send_confirmation's strings
SEND_CONFIRMATION_SUBJECT = _(u'Reset your Dentexchange')
