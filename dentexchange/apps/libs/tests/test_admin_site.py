# -*- coding:utf-8 -*-
import unittest
import mock

from ..admin import AdminSite, site


class AdminSiteTestCase(unittest.TestCase):
    def setUp(self):
        AdminSite.callbacks = []

    def test_add_callbacks_should_extend_callbacks_class_attribute(self):
        # setup
        callbacks = [mock.Mock(), mock.Mock()]

        # action
        AdminSite.add_callbacks(*callbacks)

        # assert
        self.assertListEqual(callbacks, AdminSite.callbacks)

    @mock.patch('libs.admin.BaseAdminSite.index')
    def test_index_should_call_callbacks_before_super_when_callbacks_present(
            self, index):
        # setup
        callback_1 = mock.Mock()
        callback_2 = mock.Mock()
        request = mock.Mock()
        extra_context = dict(one=1, two=2, three=3)
        site.add_callbacks(callback_1, callback_2)

        # action
        returned_value = site.index(request, extra_context=extra_context)

        # assert
        self.assertTupleEqual(((site, request,),
            dict(extra_context=extra_context)),
            callback_1.call_args)
        self.assertTupleEqual(((site, request,),
            dict(extra_context=extra_context)),
            callback_2.call_args)
        self.assertTupleEqual(((request,), dict(extra_context=extra_context)),
            index.call_args)
        self.assertEqual(id(index.return_value), id(returned_value))
