# -*- coding:utf-8 -*-
from django.conf.urls import patterns, url

from libs.decorators import login_required_for, EMPLOYEE, EMPLOYER
from membership.decorators import enforce_membership
from . import views

urlpatterns = patterns('',
    url(r'^job_postings/$',
        login_required_for(EMPLOYEE)(
        enforce_membership(views.EmployeeSearchView.as_view())),
        name='employee_search'),
    url(r'^job_postings/results/$',
        login_required_for(EMPLOYEE)(
        enforce_membership(views.EmployeeResultsView.as_view())),
        name='employee_results'),
    url(r'^employees/$',
        login_required_for(EMPLOYER)(
        enforce_membership(views.EmployerSearchView.as_view())),
        name='employer_search'),
    url(r'^employees/results/$',
        login_required_for(EMPLOYER)(
        enforce_membership(views.EmployerResultsView.as_view())),
        name='employer_results'),
    url(r'^refresh/beacon/$',
        login_required_for((EMPLOYER, EMPLOYEE))(
        enforce_membership(views.ResultsBeaconView.as_view())),
        name='results_beacon'),
)
