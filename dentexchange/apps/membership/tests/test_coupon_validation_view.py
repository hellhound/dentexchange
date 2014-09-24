# -*- coding:utf-8 -*-
import unittest
import mock

from ..views import CouponValidationView


class CouponValidationViewTestCase(unittest.TestCase):
    @mock.patch('membership.views.Coupon')
    @mock.patch('membership.views.JSONResponseMixin.render_json_response')
    def test_get_should_call_render_json_response_with_status_ok_and_discount_when_valid_coupon(
            self, render_json_response, coupon_class):
        # setup
        view = CouponValidationView()
        coupon_code = 'acouponcode'
        discount = mock.Mock()
        request = mock.Mock()
        request.GET.get.return_value = coupon_code
        view.request = request
        is_valid = coupon_class.objects.is_valid
        is_valid.return_value = True
        get_discount = coupon_class.objects.get_discount
        get_discount.return_value = discount

        # action
        response = view.get(request)

        # assert
        self.assertTupleEqual((coupon_code,), is_valid.call_args[0])
        self.assertTupleEqual((coupon_code,), get_discount.call_args[0])
        self.assertDictEqual(dict(status='ok', discount=discount),
            render_json_response.call_args[0][0])
        self.assertEqual(id(render_json_response.return_value), id(response))

    @mock.patch('membership.views.Coupon')
    @mock.patch('membership.views.JSONResponseMixin.render_json_response')
    def test_get_should_call_render_json_response_with_status_error_when_invalid_coupon(
            self, render_json_response, coupon_class):
        # setup
        view = CouponValidationView()
        coupon_code = 'aninvalidcoupon'
        request = mock.Mock()
        request.GET.get.return_value = coupon_code
        view.request = request
        is_valid = coupon_class.objects.is_valid
        is_valid.return_value = False

        # action
        response = view.get(request)

        # assert
        self.assertTupleEqual((coupon_code,), is_valid.call_args[0])
        self.assertTupleEqual((dict(status='invalid'),),
            render_json_response.call_args[0])
        self.assertEqual(id(render_json_response.return_value), id(response))

    @mock.patch('membership.views.Coupon')
    @mock.patch('membership.views.JSONResponseMixin.render_json_response')
    def test_get_should_call_render_json_response_with_status_error_when_coupon_code_not_in_request_get(
            self, render_json_response, coupon_class):
        # setup
        view = CouponValidationView()
        request = mock.Mock()
        request.GET.get.return_value = None
        view.request = request
        is_valid = coupon_class.objects.is_valid
        is_valid.return_value = False

        # action
        view.get(request)

        # assert
        self.assertTupleEqual((dict(status='invalid'),),
            render_json_response.call_args[0])
