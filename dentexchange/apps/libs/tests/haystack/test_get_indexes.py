# -*- coding:utf-8 -*-
import unittest
import mock

from ...haystack.utils import get_indexes


class GetIndexesTestCase(unittest.TestCase):
    @mock.patch('libs.haystack.utils.connections')
    @mock.patch('libs.haystack.utils.connection_router.for_write')
    def test_get_indexes_should_yield_get_index(
            self, for_write, connections):
        # setup
        model_class = mock.Mock()
        using = mock.Mock()
        for_write.return_value = [using]
        connection = mock.Mock()
        connections.__getitem__ = mock.MagicMock(return_value=connection)

        # action
        returned_value = list(get_indexes(model_class))

        # assert
        self.assertDictEqual(dict(models=[model_class]), for_write.call_args[1])
        self.assertTupleEqual((using,), connections.__getitem__.call_args[0])
        self.assertEqual(1, connection.get_unified_index.call_count)
        self.assertTupleEqual((model_class,),
            connection.get_unified_index.return_value.get_index.call_args[0])
        self.assertListEqual(
            [connection.get_unified_index.return_value.get_index.return_value],
            returned_value)
