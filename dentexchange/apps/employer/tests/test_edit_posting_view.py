# -*- coding:utf-8 -*-
import unittest
import mock

from django.http.response import Http404
from django.core.urlresolvers import reverse

from employee import constants as employee_constants
from ..views import EditPostingFormView
from ..models import Praxis, JobPosting


class EditPostingViewTestCase(unittest.TestCase):
    @mock.patch('employer.views.Praxis.objects.get')
    def test_get_should_call_render_to_response_with_job_posting_form(self,
            get):
        # setup
        view = EditPostingFormView()
        view.render_to_response = mock.Mock()
        request = mock.Mock()
        view.request = request
        view.get_object = mock.Mock(return_value=JobPosting(praxis=Praxis()))
        view.kwargs = dict(pk='1')

        # action
        view.get(request)

        # assert
        self.assertEqual(1, view.render_to_response.call_count)
        context = view.render_to_response.call_args[0][0]
        self.assertTrue('form' in context.keys())
        form = context['form']
        ### Contact Info
        self.assertTrue('position_name' in form.fields.keys())
        self.assertTrue('posting_title' in form.fields.keys())
        ### Job posting you are offering
        self.assertTrue('job_position' in form.fields.keys())
        ### Type of schedule required
        self.assertTrue('schedule_type' in form.fields.keys())
        self.assertTrue('monday_daytime' in form.fields.keys())
        self.assertTrue('monday_evening' in form.fields.keys())
        self.assertTrue('tuesday_daytime' in form.fields.keys())
        self.assertTrue('tuesday_evening' in form.fields.keys())
        self.assertTrue('wednesday_daytime' in form.fields.keys())
        self.assertTrue('wednesday_evening' in form.fields.keys())
        self.assertTrue('thursday_daytime' in form.fields.keys())
        self.assertTrue('thursday_evening' in form.fields.keys())
        self.assertTrue('friday_daytime' in form.fields.keys())
        self.assertTrue('friday_evening' in form.fields.keys())
        self.assertTrue('saturday_daytime' in form.fields.keys())
        self.assertTrue('saturday_evening' in form.fields.keys())
        self.assertTrue('sunday_daytime' in form.fields.keys())
        self.assertTrue('sunday_evening' in form.fields.keys())
        ### Compensation
        self.assertTrue('compensation_type' in form.fields.keys())
        self.assertTrue('hourly_wage' in form.fields.keys())
        self.assertTrue('annualy_wage' in form.fields.keys())
        self.assertTrue('production' in form.fields.keys())
        self.assertTrue('collection' in form.fields.keys())
        ### Experience required
        self.assertTrue('experience_years' in form.fields.keys())
        ### Benefits being offered
        self.assertTrue('benefit_1' in form.fields.keys())
        self.assertTrue('benefit_2' in form.fields.keys())
        self.assertTrue('benefit_3' in form.fields.keys())
        self.assertTrue('benefit_4' in form.fields.keys())
        self.assertTrue('benefit_5' in form.fields.keys())
        self.assertTrue('benefit_6' in form.fields.keys())
        self.assertTrue('benefit_other' in form.fields.keys())
        self.assertTrue('benefit_other_text' in form.fields.keys())
        self.assertTrue('additional_comments' in form.fields.keys())

    @mock.patch('employer.views.Praxis.objects.get')
    def test_get_should_call_template_response_with_template(self, get):
        # setup
        view = EditPostingFormView()
        request = mock.Mock()
        view.request = request
        view.get_object = mock.Mock(return_value=JobPosting(praxis=Praxis()))
        view.response_class = mock.Mock()
        view.kwargs = dict(pk='1')
        template_name = 'employer/edit_posting_form.html'

        # action
        view.get(request)

        # assert
        self.assertEqual(1, view.response_class.call_count)
        self.assertEqual(template_name,
            view.response_class.call_args[1]['template'][0])

    def test_get_sucess_url_should_redirect_to_success_url(self):
        # setup
        view = EditPostingFormView()
        praxis = mock.Mock()
        praxis.configure_mock(pk='1')
        view.object = mock.Mock()
        view.object.configure_mock(praxis=praxis)

        # action
        returned_value = view.get_success_url()

        # assert
        self.assertEqual(reverse('employer:job_posting_list',
            args=(view.object.praxis.pk,)), returned_value)

    @mock.patch('employer.views.CreateView.get_form_kwargs')
    def test_get_form_kwargs_should_put_praxis_into_kwargs_and_return_kwargs(
            self, get_form_kwargs):
        # setup
        view = EditPostingFormView()
        praxis = Praxis()
        posting = JobPosting(praxis=praxis, is_posted=True)
        view.request = mock.Mock()
        view.object = posting
        get_form_kwargs.return_value = {}

        # action
        kwargs = view.get_form_kwargs()

        # assert
        self.assertEqual(praxis, kwargs['praxis'])

    @mock.patch('employer.views.CreateView.get_form_kwargs')
    def test_get_form_kwargs_should_assign_is_posted(self,
            get_form_kwargs):
        # setup
        view = EditPostingFormView()
        praxis = Praxis()
        posting = JobPosting(praxis=praxis, is_posted=True)
        view.request = mock.Mock()
        view.object = posting
        get_form_kwargs.return_value = {}

        # action
        kwargs = view.get_form_kwargs()

        # assert
        self.assertTrue(kwargs['is_posted'])
