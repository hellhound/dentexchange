# -*- coding:utf-8 -*-
import unittest
import mock

from ...haystack.utils import AsyncIndexAdapter


class AsyncIndexAdapterTestCase(unittest.TestCase):
    @mock.patch('libs.haystack.utils.get_identifier')
    @mock.patch('libs.haystack.utils.HaystackActionTask')
    def test_remove_object_should_call_haystack_action_task_delay_with_remove_action_and_obj_identifier(
            self, haystack_action_task_class, get_identifier):
        #setup
        obj = mock.Mock()
        # action
        AsyncIndexAdapter.remove_object(obj)

        # assert
        self.assertTupleEqual((obj,), get_identifier.call_args[0])
        self.assertTupleEqual((haystack_action_task_class.REMOVE_ACTION,
            get_identifier.return_value,),
            haystack_action_task_class.delay.call_args[0])

    @mock.patch('libs.haystack.utils.get_identifier')
    @mock.patch('libs.haystack.utils.HaystackActionTask')
    def test_update_object_should_haystack_action_task_deya_with_update_action_and_obj_identifier(
            self, haystack_action_task_class, get_identifier):
        #setup
        obj = mock.Mock()
        # action
        AsyncIndexAdapter.update_object(obj)

        # assert
        self.assertTupleEqual((obj,), get_identifier.call_args[0])
        self.assertTupleEqual((haystack_action_task_class.UPDATE_ACTION,
            get_identifier.return_value,),
            haystack_action_task_class.delay.call_args[0])
