# -*- coding:utf-8 -*-
import unittest
import mock

from django.core.exceptions import ImproperlyConfigured

from ...haystack.utils import get_model_class


class GetModelClassTestCase(unittest.TestCase):
    @mock.patch('libs.haystack.utils.get_model')
    def test_get_model_class_should_return_model_class_from_object_path(
            self, get_model):
        # setup
        object_path = 'a.b.c.d.e.f'
        app_name = 'a.b.c.d.e'
        classname = 'f'

        # action
        returned_value = get_model_class(object_path)

        # assert
        self.assertTupleEqual((app_name, classname,), get_model.call_args[0])
        self.assertEqual(id(get_model.return_value), id(returned_value))

    @mock.patch('libs.haystack.utils.get_model')
    def test_get_model_class_should_raise_improperly_configured_when_get_model_returns_none(
            self, get_model):
        # setup
        object_path = 'a.b.c.d.e.f'
        app_name = 'a.b.c.d.e'
        classname = 'f'
        get_model.return_value = None

        # action
        with self.assertRaises(ImproperlyConfigured) as cm:
            returned_value = get_model_class(object_path)

        # assert
        self.assertTupleEqual((app_name, classname,), get_model.call_args[0])
        self.assertEqual('Could not load model \'%s\'.' % object_path,
            unicode(cm.exception))
