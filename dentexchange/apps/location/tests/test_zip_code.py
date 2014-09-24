# -*- coding:utf-8 -*-
import unittest
import mock
import decimal

from ..models import ZipCode


class ZipCodeTestCase(unittest.TestCase):
    def test_unicode_should_return_code(self):
        # setup
        model = ZipCode()
        code = '1.0'
        model.code = decimal.Decimal(code)

        # action
        returned_value = unicode(model)

        # assert
        self.assertEqual(code, returned_value)
