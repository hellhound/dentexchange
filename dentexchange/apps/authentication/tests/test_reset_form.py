# -*- coding:utf-8 -*-
import unittest
import mock

from django.forms import ValidationError
from ..forms import ResetForm

from .. import strings


class ResetFormTestCase(unittest.TestCase):
    @mock.patch('authentication.forms.forms.Form.clean')
    @mock.patch('authentication.forms.User')
    def test_clean_should_return_super(self, user_class, clean):
        # setup
        form = ResetForm()
        email = 'an@example.com'
        form.cleaned_data = dict(email=email)
        user_class.objects.filter.return_value.count.return_value = 1

        # action
        returned_value = form.clean()

        # assert
        self.assertDictEqual(dict(username=email),
            user_class.objects.filter.call_args[1])
        self.assertEqual(id(clean.return_value), id(returned_value))

    @mock.patch('authentication.forms.forms')
    @mock.patch('authentication.forms.User')
    def test_clean_should_raise_validation_error_when_user_not_found(
            self, user_class, forms_module):
        # setup
        form = ResetForm()
        email = 'an@example.com'
        form.cleaned_data = dict(email=email)
        user_class.objects.filter.return_value.count.return_value = 0
        forms_module.ValidationError = ValidationError

        # action
        with self.assertRaises(ValidationError) as cm:
            form.clean()

        # assert
        self.assertDictEqual(dict(username=email),
            user_class.objects.filter.call_args[1])
        self.assertEqual(strings.RESET_FORM_EMAIL_DOESNT_EXIST % email,
            cm.exception.message)
