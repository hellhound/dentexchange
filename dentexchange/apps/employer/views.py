# -*- coding:utf-8 -*-
from django.core.urlresolvers import reverse
from django.views.generic.base import View, TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.http.response import Http404
from django.contrib import messages
from django import forms

from braces import views

from libs.mixins.views import (SuccessURLAliasViewMixin, HttpRefererViewMixin,
    KwargsUserFormViewMixin)
from libs import constants as lib_constants
from libs.views.list import DentexchangeListView
from employee import constants as employee_constants
from membership.utils import MembershipRestrictionAdapter
from .forms import BusinessForm, PraxisForm, JobPostingForm
from .models import Praxis, JobPosting
from . import strings


class DeleteViewMixin(object):
    def get_ajax(self, request, *args, **kwargs):
        pk = request.GET.get('pk')
        try:
            obj = self.model.objects.get(pk=pk)
        except self.model.DoesNotExist:
            # Bad Request
            return self.render_json_response(dict(status='error'), status=400)
        obj.delete()
        return self.render_json_response(dict(status='ok'))


class DashboardView(TemplateView):
    template_name = 'employer/dashboard.html'


class BusinessFormView(SuccessURLAliasViewMixin,
        HttpRefererViewMixin, KwargsUserFormViewMixin, CreateView):
    form_class = BusinessForm
    template_name = 'employer/business_form.html'
    success_url_alias = 'membership:home'
    initial = dict(
        is_mso=lib_constants.YES_NO_CHOICES.YES)


class FirstPraxisFormView(SuccessURLAliasViewMixin,
        HttpRefererViewMixin, KwargsUserFormViewMixin, CreateView):
    form_class = PraxisForm
    template_name = 'employer/first_praxis_form.html'
    success_url_alias = 'employer:praxis_profile'


class PraxisProfileView(DentexchangeListView):
    model = Praxis
    template_name = 'employer/praxis_profile.html'

    def get_queryset(self):
        return super(PraxisProfileView, self).get_queryset().filter(
            business__user=self.request.user)


class AddNewPraxisFormView(SuccessURLAliasViewMixin, KwargsUserFormViewMixin,
        CreateView):
    form_class = PraxisForm
    template_name = 'employer/add_new_praxis_form.html'
    success_url_alias = 'employer:praxis_profile'


class EditPraxisFormView(KwargsUserFormViewMixin,
        UpdateView):
    form_class = PraxisForm
    model = Praxis
    template_name = 'employer/edit_praxis_form.html'

    def get_success_url(self):
        return reverse('employer:job_posting_list', args=(self.object.pk,))


class DeletePraxisView(DeleteViewMixin, views.JSONResponseMixin,
        views.AjaxResponseMixin, View):
    model = Praxis


class PraxisDetailView(DetailView):
    template_name = 'employer/praxis_detail.html'
    model = Praxis


class JobPostingListView(DentexchangeListView):
    model = JobPosting
    template_name = 'employer/job_posting_list.html'

    def __init__(self, *args, **kwargs):
        self._praxis = None

    @property
    def praxis(self):
        if self._praxis is None:
            praxis_pk = self.kwargs.get('pk')
            try:
                self._praxis = Praxis.objects.get(pk=praxis_pk)
            except Praxis.DoesNotExist:
                raise Http404
        return self._praxis

    def get_queryset(self):
        return super(JobPostingListView, self).get_queryset().filter(
            praxis=self.praxis)

    def get_context_data(self, **context):
        context = super(JobPostingListView, self).get_context_data(**context)
        context['praxis'] = self.praxis
        return context


class AddNewPostingFormView(SuccessURLAliasViewMixin, CreateView):
    form_class = JobPostingForm
    template_name = 'employer/add_new_posting_form.html'
    success_url_alias = 'employer:praxis_profile'
    initial = dict(
        schedule_type=employee_constants.SCHEDULE_TYPE_CHOICES.PART_TIME,
        compensation_type=\
            employee_constants.COMPENSATION_TYPE_CHOICES.HOURLY,
        visa=lib_constants.YES_NO_CHOICES.YES)

    def __init__(self, *args, **kwargs):
        super(AddNewPostingFormView, self).__init__(*args, **kwargs)
        self.praxis = None

    def dispatch_if_restriction_is_valid(self, request, *args, **kwargs):
        if MembershipRestrictionAdapter(request.user.membership
                ).verify_job_posting_restrictions():
            return super(AddNewPostingFormView, self).dispatch(request, *args,
                **kwargs)
        messages.warning(request,
            strings.ADD_NEW_POSTING_FORM_VIEW_LIMIT_EXCEEDED)
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        return self.render_to_response(self.get_context_data(form=form))

    def dispatch(self, request, *args, **kwargs):
        praxis_pk = self.kwargs.get('pk')
        try:
            self.praxis = Praxis.objects.get(pk=praxis_pk)
        except Praxis.DoesNotExist:
            raise Http404
        return self.dispatch_if_restriction_is_valid(request, *args, **kwargs)

    def form_valid(self, form):
        MembershipRestrictionAdapter(self.request.user.membership
            ).apply_job_posting_restrictions()
        return super(AddNewPostingFormView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(AddNewPostingFormView, self).get_form_kwargs()
        kwargs['praxis'] = self.praxis
        kwargs['is_posted'] = self.request.POST.get('_post_now') is not None
        return kwargs

    def get_context_data(self, **context):
        context = super(AddNewPostingFormView, self).get_context_data(**context)
        context['praxis'] = self.praxis
        return context


class EditPostingFormView(UpdateView):
    form_class = JobPostingForm
    model = JobPosting
    template_name = 'employer/edit_posting_form.html'

    def get_success_url(self):
        return reverse('employer:job_posting_list',
            args=(self.object.praxis.pk,))

    def get_form_kwargs(self):
        kwargs = super(EditPostingFormView, self).get_form_kwargs()
        kwargs['praxis'] = self.object.praxis
        kwargs['is_posted'] = self.object.is_posted
        return kwargs


class DeletePostingView(DeleteViewMixin, views.JSONResponseMixin,
        views.AjaxResponseMixin, View):
    model = JobPosting


class PostJobPostingView(views.JSONResponseMixin, views.AjaxResponseMixin,
        View):
    def get_ajax(self, request, *args, **kwargs):
        json_dict = {}
        try:
            posting = JobPosting.objects.get(pk=self.kwargs.get('pk'))
        except JobPosting.DoesNotExist:
            json_dict['status'] = 'error'
        else:
            json_dict['status'] = 'ok'
            posting.is_posted = \
                self.kwargs.get('post_status', 'offline') == 'online'
            posting.save()
        return self.render_json_response(json_dict)


class PostingDetailView(DetailView):
    template_name = 'employer/posting_detail.html'
    model = JobPosting


class PublicPostingDetailFromListView(DetailView):
    template_name = 'employer/public_posting_detail_from_list.html'
    model = JobPosting

    def get_object(self, queryset=None):
        pk = self.request.GET.get('pk')
        try:
            posting = JobPosting.objects.get(pk=pk, is_posted=True)
        except JobPosting.DoesNotExist:
            raise Http404
        return posting
