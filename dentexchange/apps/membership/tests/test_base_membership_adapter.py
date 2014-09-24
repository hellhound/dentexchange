# -*- coding:utf -*-
import unittest
import mock

from ..utils import BaseMembershipAdapter


class BaseMembershipAdapterTestCase(unittest.TestCase):
    def test_init_should_set_membership(self):
        # setup
        membership = mock.Mock()

        # action
        adapter = BaseMembershipAdapter(membership)

        # assert
        self.assertEqual(membership, adapter.membership)
