# -*- coding:utf-8 -*-
from django.views.generic import FormView, UpdateView
from django.shortcuts import redirect
from django.contrib.auth.models import User

from libs.mixins.views import SuccessURLAliasViewMixin
from .forms import ResetForm, EditPasswordForm
from .models import RecoveryToken
from .tasks import send_confirmation


class ResetFormView(SuccessURLAliasViewMixin, FormView):
    template_name = 'authentication/reset_form.html'
    form_class = ResetForm
    success_url_alias = 'authentication:successful_email_confirmation'

    def form_valid(self, form):
        send_confirmation.delay(self.request.META['HTTP_HOST'],
            form.cleaned_data['email'])
        return super(ResetFormView, self).form_valid(form)


class EditPasswordFormView(SuccessURLAliasViewMixin, UpdateView):
    form_class = EditPasswordForm
    success_url_alias = 'main:home'
    template_name = 'authentication/edit_password_form.html'
    
    def _get_token(self):
        args = self.request.POST if self.request.method.lower() == 'post' \
            else self.request.GET
        return args.get('token', None)

    def is_token_valid(self):
        token = self._get_token()
        return RecoveryToken.objects.is_token_valid(token)

    def get_object(self, queryset=None):
        return User.objects.get(recoverytoken__token=self._get_token())

    def get_initial(self):
        initial = super(EditPasswordFormView, self).get_initial()
        initial['token'] = self._get_token()
        return initial

    def get(self, request, *args, **kwargs):
        if not self.is_token_valid():
            return redirect('authentication:expired_token')
        return super(EditPasswordFormView, self).get(request, *args, **kwargs)
