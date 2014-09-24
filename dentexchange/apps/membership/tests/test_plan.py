# -*- coding:utf-8 -*-
import unittest
import mock

from ..models import Plan


class PlanTestCase(unittest.TestCase):
    def test_unicode_should_return_title(self):
        # setup
        model = Plan()
        model.title = 'atitle'

        # action
        returned_value = unicode(model) 

        # assert
        self.assertEqual(model.title, returned_value)
