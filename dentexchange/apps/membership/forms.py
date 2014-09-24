# -*- coding:utf-8 -*-
from django import forms

from form_extensions.fields import CreditCardField

from libs.mixins.forms import (MeaningfulEmptyValueFormMixin,
    UserInitializationFormMixin)
from .models import Membership, Coupon
from . import strings, constants
from .utils import (YearChoices, MembershipStripeAdapter,
    MembershipRestrictionAdapter, MembershipExpirationDateAdapter)


class BillingInfoForm(MeaningfulEmptyValueFormMixin, forms.Form):
    credit_card = CreditCardField(
        label=strings.MEMBERSHIP_CREDIT_CARD)
    cvv = forms.CharField(
        label=strings.MEMBERSHIP_CVV,
        min_length=4)
    expiry_month = forms.ChoiceField(
        label=strings.MEMBERSHIP_EXPIRY_MONTH,
        choices=constants.EXPIRY_MONTH_CHOICES)
    expiry_year = forms.ChoiceField(
        label=strings.MEMBERSHIP_EXPIRY_YEAR,
        choices=YearChoices())

    def __init__(self, *args, **kwargs):
        super(BillingInfoForm, self).__init__(*args, **kwargs)
        self.initialize_data_stripe_attributes()

    def initialize_data_stripe_attributes(self):
        for stripe_field, form_field in \
                constants.STRIPE_TO_FORM_FIELDS_MAPPING.iteritems():
            self.fields[form_field].widget.attrs.update(
                {'data-stripe': stripe_field})


class MembershipForm(MeaningfulEmptyValueFormMixin, UserInitializationFormMixin,
        forms.ModelForm):
    coupon_code = forms.CharField(label=strings.MEMBERSHIP_COUPON_CODE,
        required=False, max_length=10, min_length=10)
    # Billing Address
    zip_code = forms.DecimalField(
        label=strings.MEMBERSHIP_ZIP_CODE,
        max_digits=5, decimal_places=0,
        widget=forms.TextInput)
    non_meaningful_fields = ('plan_type',)
    stripe_token = forms.CharField(widget=forms.HiddenInput)

    class Meta(object):
        model = Membership
        exclude = ('user', 'coupon_code', 'customer_id', 'cc_last4', 'end_date',
            'remaining_job_postings')

    def clean_coupon_code(self):
        data = self.cleaned_data['coupon_code']
        if not (data is None or data.strip() == '' \
                or Coupon.objects.is_valid(data)):
            raise forms.ValidationError(
                strings.MEMBERSHIP_FORM_INVALID_COUPON_ERROR)
        return data

    def save(self, commit=True):
        cleaned_data = self.cleaned_data
        instance = super(MembershipForm, self).save(commit=False)
        if cleaned_data['coupon_code'] not in (None, ''):
            coupon = Coupon.objects.get(code=cleaned_data['coupon_code'])
            coupon.claimed_by = instance.user
            coupon.save()
            instance.coupon_code = coupon
        instance.save()
        MembershipExpirationDateAdapter(instance).save_end_date()
        MembershipRestrictionAdapter(instance).reset_restrictions()
        MembershipStripeAdapter(instance).charge_with_token(
            cleaned_data['stripe_token'])
        return instance
