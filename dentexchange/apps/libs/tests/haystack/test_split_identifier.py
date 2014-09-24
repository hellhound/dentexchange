# -*- coding:utf-8 -*-
import unittest
import mock

from ...haystack.utils import split_identifier


class SplitIdentifierTestCase(unittest.TestCase):
    def test_split_identifier_should_return_object_path_and_pk_tuple_with_identifier_as_arg(
            self):
        # setup
        object_path = 'app.model'
        pk = '1'
        identifier = '%s.%s' % (object_path, pk)

        # action
        returned_value = split_identifier(identifier)

        # assert
        self.assertTupleEqual((object_path, pk,), returned_value)

    def test_split_identifier_should_return_none_tuple_when_invalid_identifier(
            self):
        # setup
        identifier = 'something'

        # action
        returned_value = split_identifier(identifier)

        # assert
        self.assertTupleEqual((None, None,), returned_value)
