# -*- coding:utf-8 -*-
#import unittest
#import mock
#
#from libs.mixins.views import RedirectViewMixin
#
#
#class RedirectViewMixinTestCase(unittest.TestCase):
#    @mock.patch('libs.mixins.views.reverse')
#    @mock.patch('libs.mixins.views.redirect')
#    def test_get_should_call_redirect_with_redirect_url_alias(self,
#            redirect, reverse):
#        # setup
#        mixin = RedirectViewMixin()
#        mixin.redirect_url_alias = 'alias'
#        request = mock.Mock()
#        request.path = '/'
#        reverse.return_value = '/alias/'
#
#        # action
#        returned_value = mixin.get(request)
#
#        # assert
#        self.assertEqual(mixin.redirect_url_alias, reverse.call_args[0][0])
#        self.assertEqual(mixin.redirect_url_alias, redirect.call_args[0][0])
#        self.assertEqual(id(redirect.return_value), id(returned_value))
