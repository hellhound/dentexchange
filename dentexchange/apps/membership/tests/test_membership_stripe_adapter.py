# -*- coding:utf-8 -*-
import decimal
import unittest
import mock

from membership.utils import StripeFacade, MembershipStripeAdapter


class MembershipStripeAdapterTestCase(unittest.TestCase):
    def setUp(self):
        plan_type = mock.Mock()
        plan_type.price = decimal.Decimal(50.5)
        self.membership = mock.Mock()
        self.membership.configure_mock(
            plan_type=plan_type,
            customer_id=None,
            coupon_code=None,
            first_name='First Name',
            last_name='Last Name',
            email='an@example.com',
            address='123 Address',
            zip_code=12345,
            city='City',
            state='State',
            country='US')
        self.customer_id = 'acustomerid'
        self.card_token = 'atoken'

    @mock.patch('membership.utils.StripeFacade')
    def test_commit_changes_should_call_memberships_save(self,
            stripe_facade_class):
        # setup
        adapter = MembershipStripeAdapter(self.membership)
        customer = dict(id=self.customer_id)
        facade = stripe_facade_class.return_value

        # action
        adapter.commit_changes(customer)

        # assert
        self.assertEqual(self.customer_id, self.membership.customer_id)
        self.assertTupleEqual((customer,),
            facade.get_card_last_4_digits.call_args[0])
        self.assertEqual(facade.get_card_last_4_digits.return_value,
            self.membership.cc_last4)
        self.assertEqual(1, adapter.membership.save.call_count)

    @mock.patch('membership.utils.StripeFacade')
    def test_create_customer_should_facades_create_customer_with_membership_email_metadata_and_card_token(
            self, stripe_facade_class):
        # setup
        adapter = MembershipStripeAdapter(self.membership)
        metadata = dict(
            first_name=self.membership.first_name,
            last_name=self.membership.last_name,
            address=self.membership.address,
            zip_code=self.membership.zip_code,
            city=self.membership.city,
            state=self.membership.state,
            count=self.membership.country)
        facade = stripe_facade_class.return_value

        # action
        returned_value = adapter.create_customer(self.card_token)

        # assert
        self.assertTupleEqual(
            (self.membership.email, metadata, self.card_token),
            facade.create_customer.call_args[0])
        self.assertEqual(id(facade.create_customer.return_value),
        id(returned_value))

    @mock.patch('membership.utils.StripeFacade')
    def test_charge_should_call_facades_charge_customer_with_stripes_customer_and_memberships_plan_type_price_and_then_assign_stripes_customer_id_to_memberships_customer_id(
            self, stripe_facade_class):
        # setup
        adapter = MembershipStripeAdapter(self.membership)
        customer = mock.Mock()
        facade = stripe_facade_class.return_value

        # action
        adapter.charge(customer)

        # assert
        self.assertTupleEqual((customer, self.membership.plan_type.price,),
            facade.charge_customer.call_args[0])

    @mock.patch('membership.utils.StripeFacade')
    def test_charge_should_call_facades_charge_customer_with_stripes_customer_and_memberships_plant_type_price_with_applied_discount_and_then_assign_stripes_customer_id_to_memberships_customer_id(
            self, stripe_facade_class):
        # setup
        adapter = MembershipStripeAdapter(self.membership)
        coupon_code = mock.Mock()
        coupon_code.discount = decimal.Decimal(5.5)
        self.membership.coupon_code = coupon_code
        customer = mock.Mock()
        facade = stripe_facade_class.return_value

        # action
        adapter.charge(customer)

        # assert
        self.assertTupleEqual(
            (customer, self.membership.plan_type.price - coupon_code.discount,),
            facade.charge_customer.call_args[0])

    @mock.patch('membership.utils.StripeFacade')
    def test_get_customer_with_new_token_should_call_facades_get_customer_with_customer_id_the_facades_replace_default_card_with_stripes_customer_and_card_token(
            self, stripe_facade_class):
        # setup
        adapter = MembershipStripeAdapter(self.membership)
        facade = stripe_facade_class.return_value

        # action
        returned_value = adapter.get_customer_with_new_token(
            self.customer_id, self.card_token)

        # assert
        self.assertTupleEqual((self.customer_id,),
            facade.get_customer.call_args[0])
        self.assertTupleEqual(
            (facade.get_customer.return_value, self.card_token,),
            facade.replace_default_card.call_args[0])
        self.assertEqual(id(facade.get_customer.return_value),
            id(returned_value))

    @mock.patch('membership.utils.MembershipStripeAdapter.commit_changes')
    @mock.patch('membership.utils.MembershipStripeAdapter.charge')
    @mock.patch('membership.utils.MembershipStripeAdapter.create_customer')
    def test_charge_with_token_should_call_create_customer_when_memeberships_customer_id_is_none_the_call_charge_and_commit_changes_returning_true_none_tuple(
            self, create_customer, charge, commit_changes):
        # setup
        adapter = MembershipStripeAdapter(self.membership)

        # action
        returned_value = adapter.charge_with_token(self.card_token)

        # assert
        self.assertTupleEqual((self.card_token,), create_customer.call_args[0])
        self.assertTupleEqual((create_customer.return_value,),
            charge.call_args[0])
        self.assertTupleEqual((create_customer.return_value,),
            commit_changes.call_args[0])
        self.assertTupleEqual((True, None,), returned_value)

    @mock.patch('membership.utils.MembershipStripeAdapter.commit_changes')
    @mock.patch('membership.utils.MembershipStripeAdapter.charge')
    @mock.patch(
        'membership.utils.MembershipStripeAdapter.get_customer_with_new_token')
    def test_charge_with_token_should_call_get_customer_with_new_token_when_memberships_customer_id_is_not_none_the_call_charge_and_commit_changes_returning_true_none_tuple(
            self, get_customer_with_new_token, charge, commit_changes):
        # setup
        self.membership.customer_id = self.customer_id
        adapter = MembershipStripeAdapter(self.membership)

        # action
        returned_value = adapter.charge_with_token(self.card_token)

        # assert
        self.assertTupleEqual((self.customer_id, self.card_token,),
            get_customer_with_new_token.call_args[0])
        self.assertTupleEqual((get_customer_with_new_token.return_value,),
            charge.call_args[0])
        self.assertTupleEqual((get_customer_with_new_token.return_value,),
            commit_changes.call_args[0])
        self.assertTupleEqual((True, None,), returned_value)

    @mock.patch('membership.utils.MembershipStripeAdapter.create_customer')
    def test_charge_with_token_should_return_false_exception_message_tuple_when_facades_card_error_raised(
            self, create_customer):
        # setup
        adapter = MembershipStripeAdapter(self.membership)
        message = u'amessage'
        create_customer.side_effect = StripeFacade.CardError(message)

        # action
        returned_value = adapter.charge_with_token(self.card_token)

        # assert
        self.assertTupleEqual((False, message,), returned_value)

    @mock.patch('membership.utils.MembershipStripeAdapter.create_customer')
    def test_charge_with_token_should_return_false_exception_message_tuple_when_facades_generic_error_raised(
            self, create_customer):
        # setup
        adapter = MembershipStripeAdapter(self.membership)
        message = u'amessage'
        create_customer.side_effect = StripeFacade.GenericError(message)

        # action
        returned_value = adapter.charge_with_token(self.card_token)

        # assert
        self.assertTupleEqual((False, message,), returned_value)
