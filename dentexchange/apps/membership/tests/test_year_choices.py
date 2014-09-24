# -*- coding:utf-8 -*-
import unittest
import mock
import datetime

from ..utils import YearChoices


class YearChoicesTestCase(unittest.TestCase):
    def test_iter_should_return_50_years_since_current_year(self):
        # setup
        current_year = datetime.datetime.now().year
        years = range(current_year, current_year + 50)

        # action
        choices = list(YearChoices())

        # assert
        self.assertEqual(zip(years, years), choices)
