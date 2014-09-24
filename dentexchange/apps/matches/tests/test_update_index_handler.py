# -*- coding:utf-8 -*-
import unittest
import mock

from ..models import update_index_handler


class UpdateIndexHandlerTestCase(unittest.TestCase):
    @mock.patch('matches.models.AsyncIndexAdapter.update_object')
    def test_update_index_handler_should_call_async_index_adapters_update_object_with_the_instances_match_attr(
            self, update_object):
        # setup
        sender = mock.Mock()
        instance = mock.Mock()

        # action
        update_index_handler(sender, instance=instance)

        # assert
        self.assertTupleEqual((instance.match,), update_object.call_args[0])
