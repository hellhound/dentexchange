# -*- coding:utf-8 -*-
import unittest
import mock
import stripe

from django.conf import settings

from membership.utils import StripeFacade


class StripeFacadeTestCase(unittest.TestCase):
    def setUp(self):
        self.customer_values = dict(
            email='an@example.com',
            metadata=dict(somekey='somevalue'),
            card_token='atoken')

    def tearDown(self):
        StripeFacade._instance = None

    @mock.patch('membership.utils.stripe')
    def test_init_sets_stripes_api_key(self, stripe_module):
        # setup and action
        facade = StripeFacade()

        # assert
        self.assertEqual(getattr(settings, 'STRIPE_SECRET_KEY', ''),
            stripe_module.api_key)

    def test_handle_error_should_return_func(self):
        # setup
        facade = StripeFacade()
        func = mock.Mock()
        args = (1, 2)
        kwargs = dict(something='else')

        # action
        returned_value = facade.handle_error(func, *args, **kwargs)

        # assert
        self.assertTupleEqual((args, kwargs), func.call_args)
        self.assertEqual(id(func.return_value), id(returned_value))

    @mock.patch('membership.utils.stripe')
    def test_handle_error_should_raise_card_error_when_stripes_card_error_raised(
            self, stripe_module):
        # setup
        facade = StripeFacade()
        message = 'somemessage'
        func = mock.Mock()
        stripe_module.error.CardError = stripe.error.CardError
        func.side_effect = stripe.error.CardError(message, 'param', 1)

        # action
        with self.assertRaises(facade.CardError) as cm:
            facade.handle_error(func)

        # assert
        self.assertEqual(message, unicode(cm.exception))

    @mock.patch('membership.utils.stripe')
    def test_handle_error_should_raise_generic_error_when_stripes_generic_error_raised(
            self, stripe_module):
        # setup
        facade = StripeFacade()
        message = 'somemessage'
        func = mock.Mock()
        func.side_effect = stripe.error.AuthenticationError(message)

        # action
        with self.assertRaises(facade.GenericError) as cm:
            facade.handle_error(func)

        # assert
        self.assertEqual(message, unicode(cm.exception))

    @mock.patch('membership.utils.stripe')
    def test_create_customer_should_return_with_email_metadata_and_card_token(self,
            stripe_module):
        # setup
        facade = StripeFacade()

        # action
        returned_value = facade.create_customer(self.customer_values['email'],
            self.customer_values['metadata'],
            self.customer_values['card_token'])

        # assert
        self.assertDictEqual(dict(description=self.customer_values['email'],
            email=self.customer_values['email'],
            metadata=self.customer_values['metadata'],
            card=self.customer_values['card_token']),
            stripe_module.Customer.create.call_args[1])
        self.assertEqual(id(stripe_module.Customer.create.return_value),
            id(returned_value))

    @mock.patch('membership.utils.stripe')
    def test_charge_customer_should_create_stripes_charge_with_customer_and_amount(
            self, stripe_module):
        # setup
        facade = StripeFacade()
        customer = mock.Mock()
        customer.configure_mock(email=self.customer_values['email'])
        amount = 45.
        currency = 'usd'

        # action
        returned_value = facade.charge_customer(customer, amount)

        # assert
        self.assertDictEqual(dict(amount=int(amount * 100), currency=currency,
            customer=customer, description=customer.email),
            stripe_module.Charge.create.call_args[1])
        self.assertEqual(id(stripe_module.Charge.create.return_value),
            id(returned_value))

    @mock.patch('membership.utils.stripe')
    def test_get_customer_should_retrieve_stripes_customer(self, stripe_module):
        # setup
        facade = StripeFacade()
        customer_id = 'acustomerid'

        # action
        returned_value = facade.get_customer(customer_id)

        # assert
        self.assertTupleEqual((customer_id,),
            stripe_module.Customer.retrieve.call_args[0])
        self.assertEqual(id(stripe_module.Customer.retrieve.return_value),
            id(returned_value))

    def test_get_card_last_4_digits_should_return_last4_card_entry_from_customer_data(
            self):
        # setup
        facade = StripeFacade()
        card_id = 'acardid'
        last4 = '4242'
        customer = dict(
            default_card=card_id,
            cards=dict(
                data=[
                    dict(
                        id=card_id,
                        last4=last4,
                    )
                ]
            )
        )
        customer_id = 'acustomerid'

        # action
        returned_value = facade.get_card_last_4_digits(customer)

        # assert
        self.assertEqual(last4, returned_value)

    def test_replace_default_card_should_delete_default_card_then_create_new_card_with_card_token(
            self):
        # setup
        facade = StripeFacade()
        card_token = 'atoken'
        default_card_id = 'acardid'
        def customer_get_item(item):
            if item == 'default_card':
                return default_card_id
        customer = mock.MagicMock()
        customer.__getitem__.side_effect = customer_get_item

        # action
        facade.replace_default_card(customer, card_token)

        # assert
        self.assertTupleEqual((default_card_id,),
            customer.cards.retrieve.call_args[0])
        self.assertEqual(1,
            customer.cards.retrieve.return_value.delete.call_count)
        self.assertDictEqual(dict(card=card_token),
            customer.cards.create.call_args[1])
