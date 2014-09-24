# -*- coding:utf-8 -*-
import unittest
import mock
import decimal

from ..models import Coupon


class CouponManagerTestCase(unittest.TestCase):
    @mock.patch('membership.models.models.Manager.get_queryset')
    def test_is_valid_should_call_filter_with_coupon_code_and_claimed_by_as_none_then_call_count_and_return_boolean(
            self, get_queryset):
        # setup
        manager = Coupon.objects
        coupon_code = 'acouponcode'
        manager_filter = get_queryset.return_value.filter
        count = manager_filter.return_value.count
        count.return_value = 1

        # action
        returned_value = manager.is_valid(coupon_code)

        # assert
        self.assertDictEqual(dict(code=coupon_code, claimed_by__isnull=True),
            manager_filter.call_args[1])
        self.assertEqual(1, count.call_count)
        self.assertTrue(returned_value)

    @mock.patch('membership.models.models.Manager.get_queryset')
    def test_is_valid_should_return_false_when_coupon_code_is_none(
            self, get_queryset):
        # setup
        manager = Coupon.objects

        # action
        returned_value = manager.is_valid(None)

        # assert
        self.assertFalse(returned_value)

    @mock.patch('membership.models.models.Manager.get_queryset')
    def test_is_valid_should_return_false_when_coupon_code_is_none(
            self, get_queryset):
        # setup
        manager = Coupon.objects

        # action
        returned_value = manager.is_valid('')

        # assert
        self.assertFalse(returned_value)

    @mock.patch('membership.models.models.Manager.get_queryset')
    def test_get_discount_should_return_decimal_discount_from_coupon(
            self, get_queryset):
        # setup
        manager = Coupon.objects
        coupon_code = 'acouponcode'
        discount = decimal.Decimal(10.24)
        get = get_queryset.return_value.get
        coupon = get.return_value
        coupon.configure_mock(discount=discount)

        # action
        returned_value = manager.get_discount(coupon_code)

        # assert
        self.assertDictEqual(dict(code=coupon_code), get.call_args[1])
        self.assertEqual(id(discount), id(returned_value))
