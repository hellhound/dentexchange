# -*- coding:utf-8 -*-
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from . import views

urlpatterns = patterns('',
    url(r'^password_reset/$', views.ResetFormView.as_view(),
        name='password_reset'),
    url(r'^password_reset/email_confirmation/$',
        TemplateView.as_view(
        template_name='authentication/successful_email_confirmation.html'),
        name='successful_email_confirmation'),
    url(r'^password_reset/edit/$',
        views.EditPasswordFormView.as_view(), name='password_reset_edit'),
    url(r'^password_reset/expired_token/$',
        TemplateView.as_view(
        template_name='authentication/expired_token.html'),
        name='expired_token'),
)
