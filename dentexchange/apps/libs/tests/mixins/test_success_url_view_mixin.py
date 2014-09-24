# -*- coding:utf-8 -*-
import unittest
import mock

from libs.mixins.views import SuccessURLAliasViewMixin


class SuccessURLAliasViewMixinTestCase(unittest.TestCase):
    @mock.patch('libs.mixins.views.reverse')
    def test_get_success_url_should_call_reverse_with_sucess_url_alias(self,
            reverse):
        # setup
        mixin = SuccessURLAliasViewMixin()
        mixin.success_url_alias = mock.Mock()

        # action
        mixin.get_success_url()

        # assert
        self.assertEqual(id(mixin.success_url_alias),
            id(reverse.call_args[0][0]))
