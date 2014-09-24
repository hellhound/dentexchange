# -*- coding:utf-8 -*-
import unittest
import mock

from ...haystack.utils import HaystackActionTask


class HaystackActionTaskTestCase(unittest.TestCase):
    @mock.patch('libs.haystack.utils.get_indexes')
    @mock.patch('libs.haystack.utils.get_instance_from_identifier')
    def test_run_should_call_remove_object_for_each_index(
            self, get_instance_from_identifier, get_indexes):
        # setup
        task = HaystackActionTask()
        identifier = mock.Mock()
        instance = mock.Mock()
        get_instance_from_identifier.return_value = instance
        index = mock.Mock()
        get_indexes.return_value = [index]

        # action
        task.run(HaystackActionTask.REMOVE_ACTION, identifier)

        # assert
        self.assertTupleEqual((identifier,),
            get_instance_from_identifier.call_args[0])
        self.assertTupleEqual((type(instance),), get_indexes.call_args[0])
        self.assertTupleEqual((instance,), index.remove_object.call_args[0])
        self.assertEqual(0, index.update_object.call_count)

    @mock.patch('libs.haystack.utils.get_indexes')
    @mock.patch('libs.haystack.utils.get_instance_from_identifier')
    def test_run_should_call_update_object_for_each_index(
            self, get_instance_from_identifier, get_indexes):
        # setup
        task = HaystackActionTask()
        identifier = mock.Mock()
        instance = mock.Mock()
        get_instance_from_identifier.return_value = instance
        index = mock.Mock()
        get_indexes.return_value = [index]

        # action
        task.run(HaystackActionTask.UPDATE_ACTION, identifier)

        # assert
        self.assertTupleEqual((identifier,),
            get_instance_from_identifier.call_args[0])
        self.assertTupleEqual((type(instance),), get_indexes.call_args[0])
        self.assertTupleEqual((instance,), index.update_object.call_args[0])
        self.assertEqual(0, index.remove_object.call_count)
