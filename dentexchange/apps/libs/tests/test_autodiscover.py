# -*- coding:utf-8 -*-
import unittest
import mock

from ..admin import autodiscover


class AutodiscoverTestCase(unittest.TestCase):
    @mock.patch('libs.admin.base_autodiscover')
    def test_should_call_base_autodiscover(self, base_autodiscover):
        # action
        autodiscover()

        # assert
        self.assertEqual(1, base_autodiscover.call_count)
