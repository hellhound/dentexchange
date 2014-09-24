# -*- coding:utf-8 -*-
import unittest
import mock

from ..models import PlanPrice
from .. import strings
from .. import constants


class PlanPriceTestCase(unittest.TestCase):
    def test_unicode_should_return_title(self):
        # setup
        model = PlanPrice()
        model.is_free = True

        # action
        returned_value = unicode(model) 

        # assert
        self.assertEqual(unicode(strings.PLAN_PRICE_TITLE_FREE), returned_value)

    def test_title_should_return_free(self):
        # setup
        model = PlanPrice()
        model.is_free = True

        # action
        returned_value = unicode(model) 

        # assert
        self.assertEqual(unicode(strings.PLAN_PRICE_TITLE_FREE), returned_value)

    def test_title_should_return_plan_duration_in_months_singular(self):
        # setup
        model = PlanPrice()
        model.duration_magnitude = 1
        model.duration_unit = constants.DURATION_UNIT_CHOICES.MONTHS
        duration = u'1 Month'

        # action
        returned_value = unicode(model) 

        # assert
        self.assertEqual(duration, returned_value)

    def test_title_should_return_plan_duration_in_months_plural(self):
        # setup
        model = PlanPrice()
        model.duration_magnitude = 10
        model.duration_unit = constants.DURATION_UNIT_CHOICES.MONTHS
        duration = u'10 Months'

        # action
        returned_value = unicode(model) 

        # assert
        self.assertEqual(duration, returned_value)

    def test_title_should_return_plan_duration_in_years_singular(self):
        # setup
        model = PlanPrice()
        model.duration_magnitude = 1
        model.duration_unit = constants.DURATION_UNIT_CHOICES.YEARS
        duration = u'1 Year'

        # action
        returned_value = unicode(model) 

        # assert
        self.assertEqual(duration, returned_value)

    def test_title_should_return_plan_duration_in_years_plural(self):
        # setup
        model = PlanPrice()
        model.duration_magnitude = 10
        model.duration_unit = constants.DURATION_UNIT_CHOICES.YEARS
        duration = u'10 Years'

        # action
        returned_value = unicode(model) 

        # assert
        self.assertEqual(duration, returned_value)
