# -*- coding:utf-8 -*-
from django.views.generic import View
from django.views.generic.edit import CreateView
from django.core.urlresolvers import reverse

from braces.views import JSONResponseMixin, AjaxResponseMixin

from libs.mixins.views import (SuccessURLAliasViewMixin, HttpRefererViewMixin,
    KwargsUserFormViewMixin)
from .forms import BillingInfoForm, MembershipForm
from .models import Coupon, Plan


class MembershipFormView(SuccessURLAliasViewMixin, KwargsUserFormViewMixin,
        CreateView):
    form_class = MembershipForm
    template_name = 'membership/membership_form.html'
    success_url_alias = 'employee:dashboard'

    def get_success_url(self):
        if self.request.user.userregistration.is_employer:
            return reverse('employer:dashboard')
        return super(MembershipFormView, self).get_success_url()

    def get_context_data(self, **context):
        context = super(MembershipFormView, self).get_context_data(**context)
        context['billing_info_form'] = BillingInfoForm()
        context['plans'] = Plan.objects.filter(
            for_employer=self.request.user.userregistration.is_employer)
        return context


class CouponValidationView(JSONResponseMixin, AjaxResponseMixin, View):
    def get(self, request, *args, **kwargs):
        coupon_code = self.request.GET.get('coupon_code')
        if Coupon.objects.is_valid(coupon_code):
            content = dict(status='ok',
                discount=Coupon.objects.get_discount(coupon_code))
        else:
            content = dict(status='invalid')
        return self.render_json_response(content)
