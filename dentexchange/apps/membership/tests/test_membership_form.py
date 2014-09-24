# -*- coding:utf-8 -*-
import unittest
import mock
import datetime

from django import forms

from ..forms import MembershipForm
from .. import constants, strings


class MembershipFormTestCase(unittest.TestCase):
    def setUp(self):
            self.cleaned_data = dict(
            # Plan type
            plan_type=1,
            # Purchase Information
            coupon_code='1' * 50,
            # Contact Information
            first_name='First Name',
            last_name='Last Name',
            email='an@example.com',
            # Billing Info
            credit_card='1234567890123456',
            cvv='123',
            expiry_month=constants.EXPIRY_MONTH_CHOICES.MONTH_1,
            expiry_year=datetime.datetime.now().year,
            # Billing Address
            address='123 Address',
            zip_code=12345,
            city='City',
            state='Sate',
            country='US',
            stripe_token='atoken')

    @mock.patch('membership.forms.Coupon')
    def test_clean_coupon_code_should_return_coupon_code_upon_validation(self,
            coupon_class):
        # setup
        form = MembershipForm()
        form.cleaned_data = self.cleaned_data
        is_valid = coupon_class.objects.is_valid
        is_valid.return_value = True

        # action
        coupon_code = form.clean_coupon_code()

        # assert
        self.assertEqual((self.cleaned_data['coupon_code'],),
            is_valid.call_args[0])
        self.assertEqual(self.cleaned_data['coupon_code'], coupon_code)

    @mock.patch('membership.forms.Coupon')
    def test_clean_coupon_code_should_return_coupon_code_upon_validation_when_empty_string(
            self, coupon_class):
        # setup
        form = MembershipForm()
        form.cleaned_data = self.cleaned_data
        form.cleaned_data['coupon_code'] = ''
        is_valid = coupon_class.objects.is_valid
        is_valid.return_value = True

        # action
        coupon_code = form.clean_coupon_code()

        # assert
        self.assertEqual(self.cleaned_data['coupon_code'], coupon_code)

    @mock.patch('membership.forms.Coupon')
    def test_clean_coupon_code_should_return_coupon_code_upon_validation_when_white_spaces(
            self, coupon_class):
        # setup
        form = MembershipForm()
        form.cleaned_data = self.cleaned_data
        form.cleaned_data['coupon_code'] = '\t   '
        is_valid = coupon_class.objects.is_valid
        is_valid.return_value = True

        # action
        coupon_code = form.clean_coupon_code()

        # assert
        self.assertEqual(self.cleaned_data['coupon_code'], coupon_code)

    @mock.patch('membership.forms.Coupon')
    def test_clean_coupon_code_should_return_coupon_code_upon_validation_when_is_none(
            self, coupon_class):
        # setup
        form = MembershipForm()
        form.cleaned_data = self.cleaned_data
        form.cleaned_data['coupon_code'] = None
        is_valid = coupon_class.objects.is_valid
        is_valid.return_value = True

        # action
        coupon_code = form.clean_coupon_code()

        # assert
        self.assertEqual(self.cleaned_data['coupon_code'], coupon_code)

    @mock.patch('membership.forms.Coupon')
    def test_clean_coupon_code_should_raise_validation_error_when_coupon_code_is_invalid(
            self, coupon_class):
        # setup
        form = MembershipForm()
        form.cleaned_data = self.cleaned_data
        is_valid = coupon_class.objects.is_valid
        is_valid.return_value = False

        # action
        with self.assertRaises(forms.ValidationError) as cm:
            form.clean_coupon_code()

        # assert
        self.assertEqual((self.cleaned_data['coupon_code'],),
            is_valid.call_args[0])
        self.assertEqual(strings.MEMBERSHIP_FORM_INVALID_COUPON_ERROR,
            cm.exception.message)

    @mock.patch('membership.forms.MembershipStripeAdapter')
    @mock.patch('membership.forms.MembershipRestrictionAdapter')
    @mock.patch('membership.forms.MembershipExpirationDateAdapter')
    @mock.patch('membership.forms.forms.ModelForm.save')
    def test_save_should_call_super_and_return_instance_with_coupon_is_none(
            self, save, expiration_adapter_class, restriction_adapter_class,
            stripe_adapter_class):
        # setup
        form = MembershipForm()
        self.cleaned_data['coupon_code'] = None
        form.cleaned_data = self.cleaned_data
        instance = mock.Mock()
        save.return_value = instance
        instance.configure_mock(coupon_code=None)

        # action
        returned_value = form.save()

        # assert
        self.assertDictEqual(dict(commit=False), save.call_args[1])
        self.assertIsNone(returned_value.coupon_code)
        self.assertEqual(id(instance), id(returned_value))


    @mock.patch('membership.forms.MembershipStripeAdapter')
    @mock.patch('membership.forms.MembershipRestrictionAdapter')
    @mock.patch('membership.forms.MembershipExpirationDateAdapter')
    @mock.patch('membership.forms.forms.ModelForm.save')
    def test_save_should_call_super_and_return_instance_with_coupon_is_empty_string(
            self, save, expiration_adapter_class, restriction_adapter_class,
            stripe_adapter_class):
        # setup
        form = MembershipForm()
        self.cleaned_data['coupon_code'] = ''
        form.cleaned_data = self.cleaned_data
        instance = mock.Mock()
        save.return_value = instance
        instance.configure_mock(coupon_code=None)

        # action
        returned_value = form.save()

        # assert
        self.assertDictEqual(dict(commit=False), save.call_args[1])
        self.assertIsNone(returned_value.coupon_code)
        self.assertEqual(id(instance), id(returned_value))

    @mock.patch('membership.forms.MembershipStripeAdapter')
    @mock.patch('membership.forms.MembershipRestrictionAdapter')
    @mock.patch('membership.forms.MembershipExpirationDateAdapter')
    @mock.patch('membership.forms.Coupon')
    @mock.patch('membership.forms.forms.ModelForm.save')
    def test_save_should_assign_coupon_to_instance_when_coupon_is_available(
            self, save, coupon_class, expiration_adapter_class,
            restriction_adapter_class, stripe_adapter_class):
        # setup
        form = MembershipForm()
        self.cleaned_data['coupon_code'] = 'acoupon'
        form.cleaned_data = self.cleaned_data
        instance = mock.Mock()
        save.return_value = instance
        instance.configure_mock(coupon_code=None, user=mock.Mock())
        coupon = mock.Mock()
        coupon_class.objects.get.return_value = coupon

        # action
        returned_value = form.save()

        # assert
        self.assertDictEqual(dict(commit=False), save.call_args[1])
        self.assertEqual(id(instance), id(returned_value))
        self.assertDictEqual(dict(code=self.cleaned_data['coupon_code']),
            coupon_class.objects.get.call_args[1])
        self.assertEqual(id(coupon.claimed_by), id(instance.user))
        self.assertEqual(1, coupon.save.call_count)
        self.assertEqual(id(coupon), id(instance.coupon_code))
        self.assertEqual(1, instance.save.call_count)

    @mock.patch('membership.forms.MembershipStripeAdapter')
    @mock.patch('membership.forms.MembershipRestrictionAdapter')
    @mock.patch('membership.forms.MembershipExpirationDateAdapter')
    @mock.patch('membership.forms.Coupon')
    @mock.patch('membership.forms.forms.ModelForm.save')
    def test_save_should_call_membership_stripe_adapters_charge_with_token(
            self, save, coupon_class, expiration_adapter_class,
            restriction_adapter_class, stripe_adapter_class):
        # setup
        form = MembershipForm()
        form.cleaned_data = self.cleaned_data
        instance = save.return_value

        # action
        form.save()

        # assert
        self.assertTupleEqual((instance,), stripe_adapter_class.call_args[0])
        self.assertEqual(1,
            stripe_adapter_class.return_value.charge_with_token.call_count)

    @mock.patch('membership.forms.MembershipStripeAdapter')
    @mock.patch('membership.forms.MembershipRestrictionAdapter')
    @mock.patch('membership.forms.MembershipExpirationDateAdapter')
    @mock.patch('membership.forms.Coupon')
    @mock.patch('membership.forms.forms.ModelForm.save')
    def test_save_should_call_membership_expiration_adapters_save_end_date(
            self, save, coupon_class, expiration_adapter_class,
            restriction_adapter_class, stripe_adapter_class):
        # setup
        form = MembershipForm()
        form.cleaned_data = self.cleaned_data
        instance = save.return_value

        # action
        form.save()

        # assert
        self.assertTupleEqual((instance,),
            expiration_adapter_class.call_args[0])
        self.assertEqual(1,
            expiration_adapter_class.return_value.save_end_date.call_count)

    @mock.patch('membership.forms.MembershipStripeAdapter')
    @mock.patch('membership.forms.MembershipRestrictionAdapter')
    @mock.patch('membership.forms.MembershipExpirationDateAdapter')
    @mock.patch('membership.forms.Coupon')
    @mock.patch('membership.forms.forms.ModelForm.save')
    def test_save_should_call_restriction_adapters_reset_restrictions(
            self, save, coupon_class, expiration_adapter_class,
            restriction_adapter_class, stripe_adapter_class):
        # setup
        form = MembershipForm()
        form.cleaned_data = self.cleaned_data
        instance = save.return_value

        # action
        form.save()

        # assert
        self.assertTupleEqual((instance,),
            restriction_adapter_class.call_args[0])
        self.assertEqual(1,
            restriction_adapter_class.return_value.reset_restrictions.call_count
        )
