# -*- coding:utf-8 -*-
from libs.choices import Enumeration
from . import strings

USER_REGISTRATION_IS_EMPLOYER_CHOICES = Enumeration([
    (True, 'EMPLOYER', strings.IS_EMPLOYER_CHOICES_EMPLOYER),
    (False, 'EMPLOYEE', strings.IS_EMPLOYER_CHOICES_EMPLOYEE),
])

FROM_WELCOME_EMAIL = 'welcome@mailinator.com'
