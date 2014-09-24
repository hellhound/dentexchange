# -*- coding:utf-8 -*-
import datetime
import calendar
import stripe
import decimal

from itertools import izip
from collections import Iterable

from django.conf import settings
from django.utils.timezone import now

from libs.singleton import Singleton

from . import constants


class YearChoices(Iterable):
    def __iter__(self):
        year = datetime.datetime.now().year
        return izip(
            iter(xrange(year, year + 50)), 
            iter(xrange(year, year + 50)))


class StripeFacade(object):
    __metaclass__ = Singleton

    class CardError(Exception):
        pass

    class GenericError(Exception):
        pass

    def __init__(self):
        stripe.api_key = self._get_api_key()

    def _get_api_key(self):
        return getattr(settings, 'STRIPE_SECRET_KEY', '')

    def handle_error(self, func, *args, **kwargs):
        try:
            return func(*args, **kwargs)
        except stripe.error.CardError, e:
            raise self.CardError(unicode(e))
        except Exception, e:
            raise self.GenericError(unicode(e))

    def create_customer(self, email, metadata, card_token):
        return self.handle_error(stripe.Customer.create, description=email,
                email=email, metadata=metadata, card=card_token)

    def get_customer(self, customer_id):
        return self.handle_error(stripe.Customer.retrieve, customer_id)

    def replace_default_card(self, customer, card_token):
        default_card_id = customer['default_card']
        card = self.handle_error(customer.cards.retrieve, default_card_id)
        self.handle_error(card.delete)
        self.handle_error(customer.cards.create, card=card_token)

    def get_card_last_4_digits(self, customer):
        default_card_id = customer['default_card']
        card, = filter(
            lambda x: x['id'] == default_card_id, customer['cards']['data'])
        return card['last4']

    def charge_customer(self, customer, amount):
        return self.handle_error(stripe.Charge.create, amount=int(amount * 100),
            currency='usd', customer=customer, description=customer.email)


### Membership Adaters

class BaseMembershipAdapter(object):
    def __init__(self, membership):
        self._membership = membership

    @property
    def membership(self):
        return self._membership


class MembershipStripeAdapter(BaseMembershipAdapter):
    def commit_changes(self, customer):
        self.membership.customer_id = customer['id']
        self.membership.cc_last4 = StripeFacade().get_card_last_4_digits(
            customer)
        self.membership.save()

    def create_customer(self, card_token):
        metadata = dict(
            first_name=self.membership.first_name,
            last_name=self.membership.last_name,
            address=self.membership.address,
            zip_code=self.membership.zip_code,
            city=self.membership.city,
            state=self.membership.state,
            count=self.membership.country)
        customer = StripeFacade().create_customer(
            self.membership.email, metadata, card_token)
        return customer

    def charge(self, customer):
        amount = self.membership.plan_type.price
        if self.membership.coupon_code is not None:
            amount -= self.membership.coupon_code.discount
        StripeFacade().charge_customer(customer, amount)

    def get_customer_with_new_token(self, customer_id, card_token):
        facade = StripeFacade()
        customer = facade.get_customer(customer_id)
        facade.replace_default_card(customer, card_token)
        return customer

    def charge_with_token(self, card_token):
        '''
        Charges the plan - coupon and returns (bool, error_message).
        Return tuple: (True, None) if the charge was successful else
        (False, 'an error message') if something goes wrong
        '''
        facade = StripeFacade()
        try:
            if self.membership.customer_id in (None, ''):
                customer = self.create_customer(card_token)
            else:
                customer = self.get_customer_with_new_token(
                    self.membership.customer_id, card_token)
            self.charge(customer)
        except (facade.CardError, facade.GenericError), e:
            return (False, unicode(e))
        self.commit_changes(customer)
        return (True, None)


class MembershipExpirationDateAdapter(BaseMembershipAdapter):
    def save_end_date(self):
        unit = self.membership.plan_type.duration_unit
        if unit == constants.DURATION_UNIT_CHOICES.UNLIMITED:
            return
        magnitude = self.membership.plan_type.duration_magnitude
        end_date = now()
        if unit == constants.DURATION_UNIT_CHOICES.YEARS:
            year = end_date.year + magnitude
            month = end_date.month
        else:
            nonnormalized_month = end_date.month + magnitude
            year = end_date.year + nonnormalized_month / 12
            month = (nonnormalized_month - 1) % 12 + 1
        last_day = calendar.monthrange(year, month)[1]
        end_date = end_date.replace(year=year, month=month,
            day=min(end_date.day, last_day))
        self.membership.end_date = end_date
        self.membership.save()


class MembershipRestrictionAdapter(BaseMembershipAdapter):
    def reset_restrictions(self):
        if self.membership.user.userregistration.is_employer:
            self.membership.remaining_job_postings = \
                self.membership.plan_type.total_allowed_job_postings
            self.membership.save()

    def apply_job_posting_restrictions(self):
        if self.membership.remaining_job_postings == 0:
            return
        self.membership.remaining_job_postings -= 1
        self.membership.save()

    def verify_job_posting_restrictions(self):
        if self.membership.remaining_job_postings == 0:
            return False
        return True
