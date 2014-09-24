# -*- coding:utf-8 -*-
from django import forms

from django.contrib.auth.models import User

from . import strings


class ResetForm(forms.Form):
    email = forms.EmailField(label=strings.RESET_FORM_EMAIL,
        help_text=strings.RESET_FORM_EMAIL_HELP_TEXT)

    def clean(self):
        data = self.cleaned_data.get('email')
        if User.objects.filter(username=data).count() == 0:
            raise forms.ValidationError(
                strings.RESET_FORM_EMAIL_DOESNT_EXIST % data)
        return super(ResetForm, self).clean()


class EditPasswordForm(forms.ModelForm):
    confirm_password = forms.CharField(
        label=strings.EDIT_PASSWORD_FORM_CONFIRM_PASSWORD)
    token = forms.CharField(widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        super(EditPasswordForm, self).__init__(*args, **kwargs)
        for key, field in self.fields.iteritems():
            if key.endswith('password'):
                field.widget = forms.PasswordInput()

    class Meta(object):
        model = User
        fields = ('password',)

    def clean(self):
        password = self.cleaned_data.get('password', None)
        confirm_password = self.cleaned_data.get('confirm_password', None)
        if password != confirm_password:
            raise forms.ValidationError(
                strings.EDIT_PASSWORD_FORM_PASSWORD_ISNT_VALID)
        return super(EditPasswordForm, self).clean()

    def save(self, commit=True):
        instance = super(EditPasswordForm, self).save(commit=False)
        instance.set_password(self.cleaned_data['password'])
        instance.save()
        return instance
