# -*- coding:utf-8 -*-
from django import forms
from django.contrib.auth.models import User

from libs.auth.builder import UserFactory
from . import strings
from . import constants
from .models import UserRegistration


class RegistrationForm(forms.ModelForm):
    email = forms.EmailField(
        label=strings.USER_REGISTRATION_EMAIL)
    is_employer = forms.TypedChoiceField(
        choices=constants.USER_REGISTRATION_IS_EMPLOYER_CHOICES,
        coerce=lambda x: x == 'True',
        label=strings.USER_REGISTRATION_ACCOUNT_TYPE,
        widget=forms.RadioSelect)
    password = forms.CharField(
        label=strings.USER_REGISTRATION_PASSWORD,
        widget=forms.PasswordInput)
    confirm_password = forms.CharField(
        label=strings.USER_REGISTRATION_CONFIRM_PASSWORD,
        widget=forms.PasswordInput)
    terms_of_use = forms.BooleanField(
        label=strings.USER_REGISTRATION_TERMS_OF_USE, required=False)

    class Meta(object):
        model = User
        fields = ('email', 'password')

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).count() > 0:
            raise forms.ValidationError(
                strings.REGISTRATION_FORM_EMAIL_ALREADY_TAKEN)
        if UserFactory.user_exists(data):
            raise forms.ValidationError(
                strings.REGISTRATION_FORM_USERNAME_COLLISION)
        return data

    def clean_terms_of_use(self):
        data = self.cleaned_data['terms_of_use']
        if not data:
            raise forms.ValidationError(
                strings.REGISTRATION_FORM_TERMS_OF_USE_ERROR)
        return data

    def clean(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError(
                strings.REGISTRATION_FORM_PASSWORD_ISNT_VALID)
        return super(RegistrationForm, self).clean()

    def save(self, commit=True):
        data = self.cleaned_data
        self.instance = UserFactory.create_user(data['email'], data['password'])
        UserRegistration.objects.create(user=self.instance,
            is_employer=data['is_employer'])
        return self.instance
