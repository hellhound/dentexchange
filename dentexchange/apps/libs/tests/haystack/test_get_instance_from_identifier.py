# -*- coding:utf-8 -*-
import unittest
import mock

from ...haystack.utils import get_instance_from_identifier


class GetInstanceFromIdentifierTestCase(unittest.TestCase):
    def test_get_instance_from_identifier_should_return_identifier_when_identifier_is_not_instance_of_basestring(
            self):
        # setup
        identifier = mock.Mock()

        # action
        returned_value = get_instance_from_identifier(identifier)

        # assert
        self.assertEqual(id(identifier), id(returned_value))

    @mock.patch('libs.haystack.utils.get_instance')
    @mock.patch('libs.haystack.utils.get_model_class')
    @mock.patch('libs.haystack.utils.split_identifier')
    def test_get_instance_from_identifier_should_call_and_return_get_instance_upon_getting_model_class_and_pk(
            self, split_identifier, get_model_class, get_instance):
        # setup
        identifier = 'anidentifier'
        object_path = mock.Mock()
        pk = mock.Mock()
        split_identifier.return_value = (object_path, pk)

        # action
        returned_value = get_instance_from_identifier(identifier)

        # assert
        self.assertTupleEqual((identifier,), split_identifier.call_args[0])
        self.assertTupleEqual((object_path,), get_model_class.call_args[0])
        self.assertTupleEqual((get_model_class.return_value, pk,),
            get_instance.call_args[0])
        self.assertEqual(id(get_instance.return_value), id(returned_value))
