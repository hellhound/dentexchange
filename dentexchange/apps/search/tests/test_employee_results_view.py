# -*- coding:utf-8 -*-
import unittest
import mock

from haystack.query import SQ

from ..views import EmployeeResultsView
from employer.models import JobPosting
from employee import constants as employee_constants
from employee import strings as employee_strings


class EmployeeResultsViewTestCase(unittest.TestCase):
   #def setUp(self):
   #    self.obj = mock.Mock()
   #    self.obj.pk = 1
   #    self.obj.email = 'an@example.com'
   #    self.obj.obj_title = 'obj Title'
   #    self.obj.schedule_type_text = 'Schedule Type Text'
   #    self.obj.compensation_type = \
   #        employee_constants.COMPENSATION_TYPE_CHOICES.SALARY
   #    self.obj.annualy_wage_text = \
   #        employee_constants.ANNUALY_WAGE_CHOICES.ANNUALY_WAGE_1
   #    self.obj.hourly_wage_text = \
   #        employee_constants.HOURLY_WAGE_CHOICES.HOURLY_WAGE_2
   #    self.obj.job_position_text = 'Job Position Text'
   #    self.obj.address = 'Address'
   #    self.obj.state = 'State'
   #    self.obj.score = 0.15
   #    self.best_match = mock.Mock()
   #    self.best_match.score = 2.67
   #    self.was_saved = True

   #def test_get_model_should_return_job_posting_model_class(self):
   #    # setup
   #    view = EmployeeResultsView()

   #    # action
   #    returned_value = view.get_model()

   #    # assert
   #    self.assertEqual(id(JobPosting), id(returned_value))

   #def test_get_query_by_location_should_return_composite_query_by_address_zip_code_city_and_state(
   #        self):
   #    # setup
   #    view = EmployeeResultsView()
   #    location = 'a location'

   #    # action
   #    returned_value = view.get_query_by_location(location)

   #    # assert
   #    self.assertEqual(
   #        unicode(SQ(address=location) | SQ(zip_code=location) \
   #        | SQ(city=location) | SQ(state=location)),
   #        unicode(returned_value))

   #@mock.patch('search.views.urllib.quote')
   #@mock.patch('search.views.render_to_string')
   #def test_get_object_should_return_posting_dictionary_with_obj_with_compensation_type_salary(
   #        self, render_to_string, quote):
   #    # setup
   #    view = EmployeeResultsView()
   #    request = mock.Mock()
   #    view.request = request

   #    # action
   #    returned_value = view.get_object(self.obj, self.best_match,
   #        self.was_saved)

   #    # assert
   #    self.assertDictEqual(dict(
   #        pk=self.obj.pk,
   #        contact_email=self.obj.email,
   #        contact_email_subject=unicode(
   #            employee_strings.EMPLOYEE_CONTACT_SUBJECT),
   #        contact_email_body=quote.return_value,
   #        posting_title=self.obj.posting_title,
   #        schedule_type=self.obj.schedule_type_text,
   #        wage=self.obj.annualy_wage_text,
   #        job_position=self.obj.job_position_text,
   #        address=self.obj.address,
   #        state=self.obj.state,
   #        percentage=self.obj.score * 100. / self.best_match.score,
   #        score=self.obj.score,
   #        was_saved=self.was_saved),
   #        returned_value)

   #@mock.patch('search.views.urllib.quote')
   #@mock.patch('search.views.render_to_string')
   #def test_get_object_should_return_posting_dictionary_with_obj_with_compensation_type_hourly(
   #        self, render_to_string, quote):
   #    # setup
   #    view = EmployeeResultsView()
   #    request = mock.Mock()
   #    view.request = request
   #    self.obj.compensation_type = \
   #        employee_constants.COMPENSATION_TYPE_CHOICES.HOURLY

   #    # action
   #    returned_value = view.get_object(self.obj, self.best_match,
   #        self.was_saved)

   #    # assert
   #    self.assertDictEqual(dict(
   #        pk=self.obj.pk,
   #        contact_email=self.obj.email,
   #        contact_email_subject=unicode(
   #            employee_strings.EMPLOYEE_CONTACT_SUBJECT),
   #        contact_email_body=quote.return_value,
   #        posting_title=self.obj.posting_title,
   #        schedule_type=self.obj.schedule_type_text,
   #        wage=self.obj.hourly_wage_text,
   #        job_position=self.obj.job_position_text,
   #        address=self.obj.address,
   #        state=self.obj.state,
   #        percentage=self.obj.score * 100. / self.best_match.score,
   #        score=self.obj.score,
   #        was_saved=self.was_saved),
   #        returned_value)
    pass
