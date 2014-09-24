# -*- coding:utf-8 -*-
import unittest
import mock

from ..forms import PraxisForm


class FirstPraxisFormTestCase(unittest.TestCase):
    @mock.patch('employer.forms.UserInitializationFormMixin.save')
    def test_should_save_business_and_return_instance(self, save):
        # setup
        form = PraxisForm()
        user = mock.Mock()
        user.configure_mock(business=mock.Mock())
        form.user = user

        # action
        returned_value = form.save()

        # assert
        self.assertDictEqual(dict(commit=False), save.call_args[1])
        self.assertEqual(id(user.business), id(save.return_value.business))
        self.assertEqual(id(save.return_value), id(returned_value))
