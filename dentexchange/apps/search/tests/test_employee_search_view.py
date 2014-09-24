# -*- coding:utf-8 -*-
import unittest
import mock

from ..views import EmployeeSearchView


class EmployeeSearchViewTestCase(unittest.TestCase):
    def test_get_should_call_render_to_response_with_search_form(self):
        # setup
        view = EmployeeSearchView()
        view.render_to_response = mock.Mock()
        request = mock.Mock()
        view.request = request
        view.kwargs = {}

        # action
        view.get(request)

        # assert
        self.assertEqual(1, view.render_to_response.call_count)
        context = view.render_to_response.call_args[0][0]
        self.assertTrue('form' in context.keys())
        form = context['form']
        self.assertTrue('keywords' in form.fields.keys())
        self.assertTrue('location' in form.fields.keys())

    def test_get_should_call_template_response_with_template(self):
        # setup
        view = EmployeeSearchView()
        request = mock.Mock()
        view.request = request
        view.response_class = mock.Mock()
        template_name = 'search/employee_search_view.html'

        # action
        view.get(request)

        # assert
        self.assertEqual(1, view.response_class.call_count)
        self.assertEqual(template_name,
            view.response_class.call_args[1]['template'][0])

    @mock.patch('search.views.SearchFiltersForm')
    @mock.patch('search.views.SearchForm')
    @mock.patch('search.views.TemplateView.get_context_data')
    def test_get_context_data_should_put_base_tempate_on_the_context(
            self, get_context_data, search_form_class,
            search_filters_form_class):
        # setup
        view = EmployeeSearchView()
        get_context_data.return_value = {}
        base_template = 'employee/base.html'

        # action
        returned_value = view.get_context_data(**{})

        # assert
        self.assertDictEqual(dict(form=search_form_class.return_value,
            filters_form=search_filters_form_class.return_value,
            base_template=base_template), returned_value)
        self.assertEqual(id(get_context_data.return_value), id(returned_value))
