# -*- coding:utf-8 -*-
from django.views.generic.base import RedirectView
from django.core.urlresolvers import reverse

from registration.models import UserRegistration


class HomeView(RedirectView):
    def get_user_registration(self):
        return self.request.user.userregistration

    def get_redirect_url(self):
        try:
            user_registration = self.get_user_registration()
        except UserRegistration.DoesNotExist:
            return reverse('registration:home')
        if user_registration.is_employer:
            return reverse('employer:dashboard')
        return reverse('employee:dashboard')
