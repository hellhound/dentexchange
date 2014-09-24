# -*- coding:utf-8 -*-
from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse_lazy

from libs.decorators import login_required_for, EMPLOYER, EMPLOYEE
from membership.decorators import enforce_membership
from .decorators import enforce_business
from . import views

urlpatterns = patterns('',
    url(r'^$',
        login_required_for(EMPLOYER)(
        enforce_business(
        enforce_membership(
        views.DashboardView.as_view()))),
        name='dashboard'),
    url(r'^business/$',
        login_required_for(EMPLOYER)(
        views.BusinessFormView.as_view()),
        name='business'),
    url(r'^first_practice/$',
        login_required_for(EMPLOYER)(
        enforce_business(
        enforce_membership(
        views.FirstPraxisFormView.as_view()))),
        name='first_praxis'),
    url(r'^practice_profile/$',
        login_required_for(EMPLOYER)(
        enforce_business(
        enforce_membership(
        views.PraxisProfileView.as_view()))),
        name='praxis_profile'),
    url(r'^practice_profile/new/$',
        login_required_for(EMPLOYER)(
        enforce_business(
        enforce_membership(
        views.AddNewPraxisFormView.as_view()))),
        name='add_new_praxis'),
    url(r'^practice_profile/edit/(?P<pk>\d+)/$',
        login_required_for(EMPLOYER)(
        enforce_business(
        enforce_membership(
        views.EditPraxisFormView.as_view()))),
        name='edit_praxis'),
    url(r'^practice_profile/details/(?P<pk>\d+)/$',
        login_required_for(EMPLOYER)(
        enforce_business(
        enforce_membership(
        views.PraxisDetailView.as_view()))),
        name='view_praxis'),
    url(r'^praxis/delete/$',
        login_required_for(EMPLOYER)(
        enforce_business(
        enforce_membership(
        views.DeletePraxisView.as_view()))),
        name='delete_praxis'),
    url(r'^practice_profile/practice/(?P<pk>\d+)/new_posting/$',
        login_required_for(EMPLOYER)(
        enforce_business(
        enforce_membership(
        views.AddNewPostingFormView.as_view()))),
        name='add_new_posting'),
    url(r'^practice_profile/posting/edit/(?P<pk>\d+)/$',
        login_required_for(EMPLOYER)(
        enforce_business(
        enforce_membership(
        views.EditPostingFormView.as_view()))),
        name='edit_posting'),
    url(r'^practice_profile/posting/delete/$',
        login_required_for(EMPLOYER)(
        enforce_business(
        enforce_membership(
        views.DeletePostingView.as_view()))),
        name='delete_posting'),
    url(r'^practice_profile/posting/details/(?P<pk>\d+)/$',
        login_required_for(EMPLOYER)(
        enforce_business(
        enforce_membership(
        views.PostingDetailView.as_view()))),
        name='view_posting'),
    url(r'^practice_profile/practice/(?P<pk>\d+)/postings/$',
        login_required_for(EMPLOYER)(
        enforce_business(
        enforce_membership(
        views.JobPostingListView.as_view()))),
        name='job_posting_list'),
    url(r'^practice_profile/posting/(?P<pk>\d+)/(?P<post_status>\w+)/$',
        login_required_for(EMPLOYER)(
        enforce_business(
        enforce_membership(
        views.PostJobPostingView.as_view()))),
        name='post_job_posting'),
    url(r'^posting/view/$',
        login_required_for((EMPLOYER, EMPLOYEE))(
        enforce_membership(
        views.PublicPostingDetailFromListView.as_view())),
        name='view_public_posting_from_list'),
)
