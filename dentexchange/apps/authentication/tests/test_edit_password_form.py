# -*- coding:utf-8 -*-
import unittest
import mock

from django.forms import ValidationError

from authentication.forms import EditPasswordForm
from .. import strings


class EditPasswordFormTestCase(unittest.TestCase):
    def setUp(self):
        self.cleaned_data = dict(
            password='password',
            confirm_password='password',
        )

    def test_clean_should_return_cleaned_data(self):
        # setup
        form = EditPasswordForm()
        form.cleaned_data = self.cleaned_data

        # action
        returned_value = form.clean()

        # assert
        self.assertEqual(id(self.cleaned_data), id(returned_value))

    def test_clean_should_raise_validation_error_when_different_password_and_confirm_password(
            self):
        # setup
        form = EditPasswordForm()
        self.cleaned_data['confirm_password'] = 'adifferentpassword'
        form.cleaned_data = self.cleaned_data

        # action
        with self.assertRaises(ValidationError) as cm:
            form.clean()

        # assert
        self.assertEqual(
            unicode(strings.EDIT_PASSWORD_FORM_PASSWORD_ISNT_VALID),
            cm.exception.message)

    @mock.patch('authentication.forms.forms.ModelForm.save')
    def test_save_should_set_users_password_and_return_instance(self, save):
        # setup
        form = EditPasswordForm()
        cleaned_data = dict(password='password')
        form.cleaned_data = cleaned_data
        instance = mock.Mock()
        save.return_value = instance

        # action
        returned_value = form.save()

        # assert
        self.assertDictEqual(dict(commit=False), save.call_args[1])
        self.assertTupleEqual((cleaned_data['password'],),
            instance.set_password.call_args[0])
        self.assertEqual(1, instance.save.call_count)
        self.assertEqual(id(instance), id(returned_value))
