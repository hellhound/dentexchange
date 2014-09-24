#JobPosting -*- coding:utf-8 -*-
import unittest
import mock

from haystack.query import SQ

from ..views import EmployerResultsView
from employee.models import EmployeeQuestionnaire
from employee import constants as employee_constants
from employer import strings as employer_strings


class EmployerResultsViewTestCase(unittest.TestCase):
   #def setUp(self):
   #    self.obj = mock.Mock()
   #    self.obj.pk = 1
   #    self.obj.email = 'an@example.com'
   #    self.obj.schedule_type_text = 'Schedule Type Text'
   #    self.obj.compensation_type = \
   #        employee_constants.COMPENSATION_TYPE_CHOICES.SALARY
   #    self.obj.annualy_wage_text = \
   #        employee_constants.ANNUALY_WAGE_CHOICES.ANNUALY_WAGE_1
   #    self.obj.hourly_wage_text = \
   #        employee_constants.HOURLY_WAGE_CHOICES.HOURLY_WAGE_2
   #    self.obj.job_position_text = 'Job Position Text'
   #    self.obj.city = 'City'
   #    self.obj.state = 'State'
   #    self.obj.distance_text = 'Distance'
   #    self.obj.score = 0.15
   #    self.best_match = mock.Mock()
   #    self.best_match.score = 2.67
   #    self.was_saved = True

   #def test_get_model_should_return_employee_questionnaire_model_class(self):
   #    # setup
   #    view = EmployerResultsView()

   #    # action
   #    returned_value = view.get_model()

   #    # assert
   #    self.assertEqual(id(EmployeeQuestionnaire), id(returned_value))

   #def test_get_query_by_location_should_return_composite_query_by_zip_code_city_and_state(
   #        self):
   #    # setup
   #    view = EmployerResultsView()
   #    location = 'a location'

   #    # action
   #    returned_value = view.get_query_by_location(location)

   #    # assert
   #    self.assertEqual(
   #        unicode(SQ(zip_code=location) \
   #        | SQ(city=location) | SQ(state=location)),
   #        unicode(returned_value))

   #@mock.patch('search.views.urllib.quote')
   #@mock.patch('search.views.render_to_string')
   #def test_get_object_should_return_questionnaire_dictionary_with_obj_with_compensation_type_salary(
   #        self, render_to_string, quote):
   #    # setup
   #    view = EmployerResultsView()

   #    # action
   #    returned_value = view.get_object(self.obj, self.best_match,
   #        self.was_saved)

   #    # assert
   #    self.assertDictEqual(dict(
   #        pk=self.obj.pk,
   #        contact_email=self.obj.email,
   #        contact_email_subject=unicode(
   #            employer_strings.EMPLOYER_CONTACT_SUBJECT),
   #        contact_email_body=quote.return_value,
   #        schedule_type=self.obj.schedule_type_text,
   #        wage=self.obj.annualy_wage_text,
   #        job_position=self.obj.job_position_text,
   #        city=self.obj.city,
   #        state=self.obj.state,
   #        distance=self.obj.distance_text,
   #        percentage=self.obj.score * 100. / self.best_match.score,
   #        score=self.obj.score,
   #        was_saved=self.was_saved),
   #        returned_value)

   #@mock.patch('search.views.urllib.quote')
   #@mock.patch('search.views.render_to_string')
   #def test_get_object_should_return_questionnaire_dictionary_with_obj_with_compensation_type_hourly(
   #        self, render_to_string, quote):
   #    # setup
   #    view = EmployerResultsView()
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
   #            employer_strings.EMPLOYER_CONTACT_SUBJECT),
   #        contact_email_body=quote.return_value,
   #        schedule_type=self.obj.schedule_type_text,
   #        wage=self.obj.hourly_wage_text,
   #        job_position=self.obj.job_position_text,
   #        city=self.obj.city,
   #        state=self.obj.state,
   #        distance=self.obj.distance_text,
   #        percentage=self.obj.score * 100. / self.best_match.score,
   #        score=self.obj.score,
   #        was_saved=self.was_saved),
   #        returned_value)
    pass
