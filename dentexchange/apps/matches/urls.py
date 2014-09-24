# -*- coding:utf-8 -*-
from django.conf.urls import patterns, url

from libs.decorators import login_required_for, EMPLOYEE, EMPLOYER
from membership.decorators import enforce_membership
from . import views

urlpatterns = patterns('',
    url(r'^add/questionnaire/$',
        login_required_for(EMPLOYER)(
        enforce_membership(views.AddQuestionnaireMatchView.as_view())),
        name='add_questionnaire_match'),
    url(r'^add/job_posting/$',
        login_required_for(EMPLOYEE)(
        enforce_membership(views.AddJobPostingMatchView.as_view())),
        name='add_job_posting_match'),
    url(r'^delete/questionnaire/$',
        login_required_for(EMPLOYER)(
        enforce_membership(views.DeleteQuestionnaireMatchView.as_view())),
        name='delete_questionnaire_match'),
    url(r'^delete/job_posting/$',
        login_required_for(EMPLOYEE)(
        enforce_membership(views.DeleteJobPostingMatchView.as_view())),
        name='delete_job_posting_match'),
    url(r'^save/automatch/$',
        login_required_for((EMPLOYEE, EMPLOYER))(
        enforce_membership(views.AddFromAutomatchView.as_view())),
        name='add_match_from_automatch'),
    url(r'^delete/automatch/$',
        login_required_for((EMPLOYEE, EMPLOYER))(
        enforce_membership(views.DeleteFromAutomatchView.as_view())),
        name='delete_match_from_automatch'),
    url(r'^saved_matches/questionnaire/$',
        login_required_for(EMPLOYER)(
        enforce_membership(views.QuestionnaireSavedMatchesView.as_view())),
        name='questionnaire_saved_matches'),
    url(r'^saved_matches/job_posting/$',
        login_required_for(EMPLOYEE)(
        enforce_membership(views.JobPostingSavedMatchesView.as_view())),
        name='job_posting_saved_matches'),
    url(r'^automatches/questionnaire/$',
        login_required_for(EMPLOYER)(
        enforce_membership(views.QuestionnaireAutomatchesView.as_view())),
        name='questionnaire_automatches'),
    url(r'^automatches/job_posting/$',
        login_required_for(EMPLOYEE)(
        enforce_membership(views.JobPostingAutomatchesView.as_view())),
        name='job_posting_automatches'),
    url(r'^automatches/refresh/$',
        login_required_for((EMPLOYER, EMPLOYEE))(
        enforce_membership(views.RefreshAutomatchView.as_view())),
        name='refresh_automatches'),
    url(r'^automatches/refresh/beacon/$',
        login_required_for((EMPLOYER, EMPLOYEE))(
        enforce_membership(views.RefreshAutomatchBeaconView.as_view())),
        name='refresh_automatches_beacon'),
)
