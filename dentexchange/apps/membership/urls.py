# -*- coding:utf-8 -*-
from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse_lazy
from django.views.generic.base import TemplateView

from libs.decorators import login_required_for, EMPLOYEE, EMPLOYER
from . import views

urlpatterns = patterns('',
    url( r'^$',
        login_required_for((EMPLOYEE, EMPLOYER))(
        views.MembershipFormView.as_view()),
        name='home'),
    url(r'^coupon_validation/$',
        login_required_for((EMPLOYEE, EMPLOYER))(
        views.CouponValidationView.as_view()),
        name='coupon_validation'),
    url(r'^employee/current_plan/$',
        login_required_for(EMPLOYEE)(
        TemplateView.as_view(
            template_name='membership/employee_current_plan.html')),
        name='employee_current_plan'),
    url(r'^employer/current_plan/$',
        login_required_for(EMPLOYER)(
        TemplateView.as_view(
            template_name='membership/employer_current_plan.html')),
        name='employer_current_plan'),
)
