# -*- coding:utf-8 -*-
import unittest
import mock

from ..forms import BusinessForm


class BusinessFormTestCase(unittest.TestCase):
    def setUp(self):
        self.cleaned_data = dict(
            ### Personal Info
            first_name='First Name',
            last_name='Last Name',
            personal_address='123 Address',
            personal_zip_code=12345,
            personal_city='City',
            personal_state='State')

    @mock.patch('employer.forms.UserInitializationFormMixin.save')
    def test_save_should_call_super_and_return_instance(self, save):
        # setup
        form = BusinessForm()
        form._save_personal_info = mock.Mock()

        # action
        returned_value = form.save()

        # assert
        self.assertDictEqual(dict(commit=True), save.call_args[1])
        self.assertEqual(id(save.return_value), id(returned_value))

    @mock.patch('employer.forms.UserInitializationFormMixin.save')
    def test_save_should_save_personal_info_fields(self, save):
        # setup
        user = mock.Mock()
        instance = mock.Mock()
        instance.user = user
        user_registration = mock.Mock()
        user.configure_mock(userregistration=user_registration)
        form = BusinessForm(user=user)
        form.cleaned_data = self.cleaned_data
        save.return_value = instance

        # action
        form.save()

        # assert
        self.assertEqual(self.cleaned_data['first_name'],
            user_registration.first_name)
        self.assertEqual(self.cleaned_data['last_name'],
            user_registration.last_name)
        self.assertEqual(self.cleaned_data['personal_address'],
            user_registration.personal_address)
        self.assertEqual(self.cleaned_data['personal_zip_code'],
            user_registration.personal_zip_code)
        self.assertEqual(self.cleaned_data['personal_city'],
            user_registration.personal_city)
        self.assertEqual(self.cleaned_data['personal_state'],
            user_registration.personal_state)
        self.assertEqual(1, user_registration.save.call_count)
