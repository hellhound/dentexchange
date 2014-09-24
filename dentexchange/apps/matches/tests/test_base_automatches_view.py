# -*- coding:utf-8 -*-
import unittest
import mock

from ..views import BaseAutomatchesView


class BaseAutomatchesViewTestCase(unittest.TestCase):
    @mock.patch('matches.views.Automatch.objects.filter')
    def test_get_queryset_should_returned_filtered_automatches_queryset_by_user(
            self, automatch_filter):
        # setup
        view = BaseAutomatchesView()
        request = mock.Mock()
        view.request = request

        # action
        returned_value = view.get_queryset()

        # assert
        self.assertDictEqual(dict(user=request.user),
            automatch_filter.call_args[1])
        self.assertEqual(id(automatch_filter.return_value), id(returned_value))
