# -*- coding:utf-8 -*-
import unittest
import mock

from ...haystack.utils import get_instance


class GetInstanceTestCase(unittest.TestCase):
    def test_get_instance_should_call_and_return_managers_get_with_pk_from_model_class(
            self):
        # setup
        model_class = mock.Mock()
        pk = '1'
        get = model_class._default_manager.get

        # action
        returned_value = get_instance(model_class, pk)

        # assert
        self.assertDictEqual(dict(pk=int(pk)), get.call_args[1])
        self.assertEqual(id(get.return_value), id(returned_value))

    def test_get_instance_should_return_none_when_pk_does_not_exist(
            self):
        # setup
        model_class = mock.Mock()
        pk = '1'
        get = model_class._default_manager.get
        model_class.DoesNotExist = Exception
        get.side_effect = model_class.DoesNotExist()

        # action
        returned_value = get_instance(model_class, pk)

        # assert
        self.assertDictEqual(dict(pk=int(pk)), get.call_args[1])
        self.assertIsNone(returned_value)

    def test_get_instance_should_return_none_when_pk_yields_multiple_objects(
            self):
        # setup
        model_class = mock.Mock()
        pk = '1'
        get = model_class._default_manager.get
        model_class.MultipleObjectsReturned = Exception
        get.side_effect = model_class.MultipleObjectsReturned()

        # action
        returned_value = get_instance(model_class, pk)

        # assert
        self.assertDictEqual(dict(pk=int(pk)), get.call_args[1])
        self.assertIsNone(returned_value)
