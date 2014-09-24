# -*- coding:utf-8 -*-
import unittest
import mock

from ..decorators import enforce_business
from ..models import Business


class EnforceBusinessTestCase(unittest.TestCase):
    def test_enforce_business_should_execute_and_return_view(self):
        # setup
        view = mock.Mock()
        wrapped_view = enforce_business(view)
        request = mock.Mock()
        args = (1, 2, 3,)
        kwargs = dict(one=1, two=2, three=3)

        # action
        returned_value = wrapped_view(request, *args, **kwargs)

        # assert
        self.assertTupleEqual(((request,) + args, kwargs,), view.call_args)
        self.assertEqual(id(view.return_value), id(returned_value))

    @mock.patch('employer.decorators.redirect')
    def test_enforce_business_should_redirect_to_business_area_when_the_user_doesnt_have_a_business(
            self, redirect):
        # setup
        class UserMock(mock.Mock):
            @property
            def business(self):
                raise Business.DoesNotExist()

        view = mock.Mock()
        wrapped_view = enforce_business(view)
        request = mock.Mock()
        request.user = UserMock()

        # action
        returned_value = wrapped_view(request)

        # assert
        self.assertTupleEqual(('employer:business',), redirect.call_args[0])
        self.assertEqual(0, view.call_count)
        self.assertEqual(id(redirect.return_value), id(returned_value))
