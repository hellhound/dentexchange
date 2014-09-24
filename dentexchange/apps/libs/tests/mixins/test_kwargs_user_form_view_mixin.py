# -*- coding:utf-8 -*-
import unittest
import mock

from ...mixins.views import KwargsUserFormViewMixin


class KwargsUserFormViewMixinTestCase(unittest.TestCase):
    @mock.patch('libs.mixins.views.Mixin.base_impl')
    def test_get_form_kwargs_should_return_kwargs_with_user(self,
            base_impl):
        # setup
        mixin = KwargsUserFormViewMixin()
        base_impl.return_value = mock.Mock()
        base_impl.return_value.get_form_kwargs.return_value = {}
        user = mock.Mock()
        request = mock.Mock()
        request.configure_mock(user=user)
        mixin.request = request

        # action
        kwargs = mixin.get_form_kwargs()

        # assert
        self.assertDictEqual(dict(user=user), kwargs)
