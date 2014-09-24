# -*- coding:utf-8 -*-
import unittest
import mock

from libs.mixins.forms import MeaningfulEmptyValueFormMixin
from ... import strings


class MeaningfulEmptyValueFormMixinTestCase(unittest.TestCase):
    @mock.patch('libs.mixins.forms.MeaningfulEmptyValueFormMixin.'
        'initialize_empty_values')
    def test_init_should_call_initialize_empty_values(self,
            initialize_empty_values):
        # setup and action
        mixin = MeaningfulEmptyValueFormMixin()

        # assert
        self.assertEqual(1, initialize_empty_values.call_count)

    @mock.patch('libs.mixins.forms.MeaningfulEmptyValueFormMixin.__init__')
    def test_initialize_empty_values_should_replace_empty_value_with_a_meaningful_one(self,
            __init__):
        # setup
        __init__.return_value = None
        mixin = MeaningfulEmptyValueFormMixin()
        label = u'Label'
        original_choices = [
            (u'', u'----'),
            (u'', u'Something else'),
        ]
        modified_choices = [
            (u'', strings.MEANINGFUL_EMPTY_VALUE_FORM_LABEL % label),
            (u'', u'Something else'),
        ]
        field = mock.Mock()
        field.configure_mock(choices=original_choices, label=label)
        def getitem(key):
            return field
        fields = mock.MagicMock()
        fields.__getitem__.side_effect=getitem
        fields.keys.return_value = ['key']
        mixin.fields = fields

        # action
        mixin.initialize_empty_values()

        # assert
        self.assertListEqual(modified_choices, field.choices)
        self.assertListEqual(modified_choices, field.widget.choices)

    @mock.patch('libs.mixins.forms.MeaningfulEmptyValueFormMixin.__init__')
    def test_initialize_empty_values_should_avoid_replacing_empty_value_when_non_meaningful_fields_are_present(
            self, __init__):
        # setup
        __init__.return_value = None
        mixin = MeaningfulEmptyValueFormMixin()
        mixin.non_meaningful_fields = ('somefield',)
        label = u'Label'
        original_choices = [
            (u'', u'----'),
            (u'', u'Something else'),
        ]
        modified_choices = [
            (u'', u'----'),
            (u'', u'Something else'),
        ]
        field = mock.Mock()
        field.configure_mock(choices=original_choices, label=label)
        def getitem(key):
            return field
        fields = mock.MagicMock()
        fields.__getitem__.side_effect=getitem
        fields.keys.return_value = ['somefield']
        mixin.fields = fields

        # action
        mixin.initialize_empty_values()

        # assert
        self.assertListEqual(modified_choices, field.choices)
