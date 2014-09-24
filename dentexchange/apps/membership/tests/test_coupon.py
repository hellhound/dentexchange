# -*- coding:utf-8 -*-
import unittest
import mock

from django.contrib.auth.models import User

from ..models import Coupon, Membership
from .. import strings


class CouponTestCase(unittest.TestCase):
    def test_unicode_should_return_code_and_user_unicode_when_claimed(self):
        # setup
        model = Coupon()
        model.code = '1234567890'
        model.claimed_by = User(username='an@example.com')

        # action
        returned_value = unicode(model)

        # assert
        self.assertEqual(strings.COUPON_CLAIMED_UNICODE % (
            model.code, model.claimed_by), returned_value)

    def test_unicode_should_return_only_code_when_unclaimed(self):
        # setup
        Coupon.claimed_by = property(
            mock.Mock(side_effect=Membership.DoesNotExist))
        model = Coupon()
        model.code = '1234567890'

        # action
        returned_value = unicode(model)

        # assert
        self.assertEqual(strings.COUPON_UNCLAIMED_UNICODE % model.code,
            returned_value)

    def test_get_email_should_return_email(self):
        # setup
        model = Coupon()
        model.claimed_by = User(email='an@example.com')

        # action
        email = model.get_email()

        # assert
        self.assertEqual(model.claimed_by.email, email)

    def test_objects_references_coupon_manager(self):
        # assert
        self.assertEqual('CouponManager', type(Coupon.objects).__name__)

    @mock.patch('membership.models.models.Model.save')
    @mock.patch('membership.models.uuid4')
    @mock.patch('membership.models.hashlib')
    def test_save_should_generate_coupon_code_before_saving_if_pk_is_none(self,
            hashlib_module, uuid4, save):
        # setup
        model = Coupon()
        model.pk = None
        uuid4_str = 'uuid4'
        uuid4.return_value.__unicode__ = mock.MagicMock(return_value=uuid4_str)
        hexdigest = hashlib_module.sha512.return_value.hexdigest
        hexdigest.return_value.__getslice__ = mock.MagicMock()

        # action
        model.save()

        # assert
        self.assertEqual(1, uuid4.call_count)
        self.assertTupleEqual((uuid4_str,), hashlib_module.sha512.call_args[0])
        self.assertEqual(1, hexdigest.call_count)
        self.assertTupleEqual((0, 10),
            hexdigest.return_value.__getslice__.call_args[0])
        self.assertEqual(id(model.code), id(
            hexdigest.return_value.__getslice__.return_value.upper.return_value)
        )
        self.assertEqual(1, save.call_count)

    @mock.patch('membership.models.models.Model.save')
    @mock.patch('membership.models.uuid4')
    @mock.patch('membership.models.hashlib')
    def test_save_should_not_generate_coupon_code_if_pk_is_not_none(self,
            hashlib_module, uuid4, save):
        # setup
        model = Coupon()
        model.pk = 1

        # action
        model.save()

        # assert
        self.assertEqual('', model.code)
