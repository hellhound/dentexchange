# -*- coding:utf-8 -*-
from django.conf.urls import patterns, url

from libs.decorators import login_required_for, EMPLOYEE, EMPLOYER
from membership.decorators import enforce_membership
from . import views

urlpatterns = patterns('',
    url(r'^$',
        login_required_for(EMPLOYEE)(
        enforce_membership(views.DashboardView.as_view())),
        name='dashboard'),
    url(r'^questionnaire/$',
        login_required_for(EMPLOYEE)(
        views.AddEmployeeQuestionnaireFromSignUpFormView.as_view()),
        name='questionnaire_signup_add'),
    url(r'^questionnaire/edit/(?P<pk>\d+)/$',
        login_required_for(EMPLOYEE)(enforce_membership(
        views.EditEmployeeQuestionnaireFromProfileFormView.as_view())),
        name='questionnaire_edit'),
    url(r'^questionnaire/add/$',
        login_required_for(EMPLOYEE)(enforce_membership(
        views.AddEmployeeQuestionnaireFromProfileFormView.as_view())),
        name='questionnaire_add'),
    url(r'^questionnaire/view/$',
        login_required_for((EMPLOYER, EMPLOYEE))(enforce_membership(
            views.PublicQuestionnaireDetailFromListView.as_view())),
        name='view_public_questionnaire_from_list'),
)
