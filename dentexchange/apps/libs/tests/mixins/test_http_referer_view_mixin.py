# -*- coding:utf-8 -*-
import unittest
import mock

from django.http.response import HttpResponseBadRequest

from libs.mixins.views import HttpRefererViewMixin
from libs import strings


class HttpRefererViewMixinTestCase(unittest.TestCase):
    def test_get_should_return_bad_request_response_when_referer_is_not_none_and_different_from_meta_referer(
            self):
        # setup
        mixin = HttpRefererViewMixin()
        request = mock.Mock()
        from_referer = '/something/'
        request.META = dict(HTTP_REFERER=from_referer)
        mixin.request = request
        to_referer = mock.MagicMock()
        to_referer.__unicode__ = mock.Mock(return_value='/something-else/')

        # action
        response = mixin.get(request, referers=(to_referer,))

        # assert
        self.assertIsInstance(response, HttpResponseBadRequest)
        self.assertEqual(
            strings.HTTP_REFERER_VIEW_MIXIN_FORM_VIEW_BAD_REQUEST \
            % from_referer,
            response.content)

    @mock.patch('libs.mixins.views.Mixin.base_impl')
    def test_get_should_return_super_get_when_referer_is_none(self, base_impl):
        # setup
        mixin = HttpRefererViewMixin()
        request = mock.Mock()
        from_referer = '/something/'
        request.META = dict(HTTP_REFERER=from_referer)
        mixin.request = request

        # action
        response = mixin.get(request)

        # assert
        self.assertEqual(id(base_impl.return_value.get.return_value),
            id(response))

    @mock.patch('libs.mixins.views.Mixin.base_impl')
    def test_get_should_return_super_get_when_referer_is_the_same_as_from_meta_referer(
            self, base_impl):
        # setup
        mixin = HttpRefererViewMixin()
        request = mock.Mock()
        from_referer = '/something/'
        request.META = dict(HTTP_REFERER=from_referer)
        mixin.request = request
        to_referer = mock.MagicMock()
        to_referer.__unicode__ = mock.Mock(return_value='/something/')
        to_referer2 = mock.MagicMock()
        to_referer2.__unicode__ = mock.Mock(return_value='/something-else/')

        # action
        response = mixin.get(request, referers=(to_referer, to_referer2,))

        # assert
        self.assertEqual(id(base_impl.return_value.get.return_value),
            id(response))
