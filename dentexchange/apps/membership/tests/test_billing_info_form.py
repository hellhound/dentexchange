# -*- coding:utf-8 -*-
import unittest
import mock

from ..forms import BillingInfoForm


class BillingInfoFormTestCase(unittest.TestCase):
    @mock.patch('membership.forms.constants')
    @mock.patch('membership.forms.forms.Form.__init__')
    @mock.patch('membership.forms.MeaningfulEmptyValueFormMixin.__init__')
    def test_initialize_data_stripe_attributes_should_add_data_stripe_attribute_to_every_field_widget(
            self, mixin__init__, __init__, constants):
        # setup
        __init__.return_value = None
        form = BillingInfoForm()
        stripe_field = 'somestripefield'
        form_field = 'someformfield'
        constants.STRIPE_TO_FORM_FIELDS_MAPPING = {
            stripe_field: form_field
        }
        field = mock.Mock()
        field.widget.attrs = {}
        form.fields = {form_field: field}

        # action
        form.initialize_data_stripe_attributes()

        # assert
        self.assertDictEqual({'data-stripe': stripe_field}, field.widget.attrs)
