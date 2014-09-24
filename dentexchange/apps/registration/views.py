# -*- coding:utf-8 -*-
from django.views.generic.edit import CreateView
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect

from libs.mixins.views import SuccessURLAliasViewMixin
from .forms import RegistrationForm
from .tasks import send_welcome_message
from . import constants


class RegistrationFormView(SuccessURLAliasViewMixin,
        CreateView):
    form_class = RegistrationForm
    template_name = 'registration/registration_form.html'
    success_url_alias = 'employee:questionnaire_signup_add'
    initial = dict(
        is_employer=constants.USER_REGISTRATION_IS_EMPLOYER_CHOICES.EMPLOYER)

    def form_valid(self, form):
        response = super(RegistrationFormView, self).form_valid(form)
        user = authenticate(
            username=form.cleaned_data['email'],
            password=form.cleaned_data['password'])
        login(self.request, user)
        send_welcome_message.delay(self.request.META['HTTP_HOST'],
            form.cleaned_data['email'])
        if form.cleaned_data['is_employer']:
            return redirect('employer:business')
        return response
