# -*- coding:utf-8 -*-
import unittest
import mock

from django.forms import ValidationError

from ..forms import RegistrationForm
from .. import strings


class RegistrationFormTestCase(unittest.TestCase):
    def setUp(self):
        self.cleaned_data = dict(
            email='example@example.com',
            is_employer=False,
            password='123',
            confirm_password='123',
            terms_of_use=True
        )

    def test_clean_should_succeed_validation(self):
        # setup
        form = RegistrationForm()
        form.cleaned_data = self.cleaned_data

        # action
        cleaned_data = form.clean()

        # assert
        self.assertDictEqual(self.cleaned_data, cleaned_data)

    def test_clean_should_raise_validation_error_when_password_and_confirm_password_are_different(self):
        # setup
        form = RegistrationForm()
        self.cleaned_data['confirm_password'] = '12'
        form.cleaned_data = self.cleaned_data

        # action
        with self.assertRaises(ValidationError) as cm:
            form.clean()

        # assert
        self.assertEqual(strings.REGISTRATION_FORM_PASSWORD_ISNT_VALID,
            cm.exception.message)

    @mock.patch('registration.forms.UserRegistration')
    @mock.patch('registration.forms.UserFactory.create_user')
    @mock.patch('registration.forms.forms.ModelForm.save')
    def test_save_should_save_and_return_user(self, super_save, create_user,
            user_registration_class):
        # setup
        form = RegistrationForm()
        instance = mock.Mock()
        form.cleaned_data = self.cleaned_data
        user_registration_class.objects.create = mock.Mock()
        super_save.return_value = form.instance

        # action
        user = form.save(commit=True)

        # assert
        self.assertTupleEqual(
            (self.cleaned_data['email'], self.cleaned_data['password'],),
            create_user.call_args[0])
        self.assertDictEqual(
            dict(user=form.instance,
            is_employer=self.cleaned_data['is_employer']),
            user_registration_class.objects.create.call_args[1])
        self.assertEqual(id(create_user.return_value), id(user))

    @mock.patch('registration.forms.User')
    def test_clean_email_should_raise_validation_error_when_the_email_is_already_taken(self,
            user_registration_class):
        # setup
        form = RegistrationForm()
        form.cleaned_data = self.cleaned_data
        user_registration_class.objects.filter = mock.Mock(
            return_value=mock.Mock())
        user_registration_class.objects.filter().configure_mock(
            count=mock.Mock(return_value=1))

        # action
        with self.assertRaises(ValidationError) as cm:
            form.clean_email()

        # assert
        self.assertEqual(strings.REGISTRATION_FORM_EMAIL_ALREADY_TAKEN,
            cm.exception.message)

    @mock.patch('registration.forms.UserFactory.user_exists')
    @mock.patch('registration.forms.User')
    def test_clean_email_should_raise_validation_error_when_a_username_collision_happens(
            self, user_registration_class, user_exists):
        # setup
        form = RegistrationForm()
        form.cleaned_data = self.cleaned_data
        user_registration_class.objects.filter = mock.Mock(
            return_value=mock.Mock())
        user_registration_class.objects.filter().configure_mock(
            count=mock.Mock(return_value=0))
        user_exists.return_value = True

        # action
        with self.assertRaises(ValidationError) as cm:
            form.clean_email()

        # assert
        self.assertEqual(strings.REGISTRATION_FORM_USERNAME_COLLISION,
            cm.exception.message)

    @mock.patch('registration.forms.UserFactory.user_exists')
    @mock.patch('registration.forms.User')
    def test_clean_email_should_succeed_validation(self,
            user_registration_class, user_exists):
        # setup
        form = RegistrationForm()
        form.cleaned_data = self.cleaned_data
        user_registration_class.objects.filter = mock.Mock(
            return_value=mock.Mock())
        user_registration_class.objects.filter().configure_mock(
            count=mock.Mock(return_value=0))
        user_exists.return_value = False

        # action
        email = form.clean_email()

        # assert
        self.assertEqual(self.cleaned_data['email'], email)

    def test_clean_terms_of_use_should_fail_validation(self):
        # setup
        form = RegistrationForm()
        self.cleaned_data['terms_of_use'] = False
        form.cleaned_data = self.cleaned_data

        # action
        with self.assertRaises(ValidationError) as cm:
            form.clean_terms_of_use()

        # assert
        self.assertEqual(strings.REGISTRATION_FORM_TERMS_OF_USE_ERROR,
            cm.exception.message)

    def test_clean_terms_of_use_should_succeed_validation(self):
        # setup
        form = RegistrationForm()
        form.cleaned_data = self.cleaned_data

        # action
        terms_of_use = form.clean_terms_of_use()

        # assert
        self.assertTrue(terms_of_use)
