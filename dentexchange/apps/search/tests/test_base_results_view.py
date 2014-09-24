# -*- coding:utf-8 -*-
import unittest
import mock

from haystack.query import SQ
from haystack.inputs import Clean

from libs import constants as libs_constants
from ..views import BaseResultsView


class BaseResultsViewTestCase(unittest.TestCase):
   #def test_get_paginate_by_should_return_libs_constants_paginated_by(self):
   #    # setup
   #    view = BaseResultsView()
   #    queryset = mock.Mock()

   #    # action
   #    returned_value = view.get_paginate_by(queryset)

   #    # assert
   #    self.assertEqual(libs_constants.PAGINATE_BY, returned_value)

   #def test_get_filtered_queryset_should_call_and_return_queryset_filter_with_query(
   #        self):
   #    # setup
   #    view = BaseResultsView()
   #    queryset = mock.Mock()
   #    query = mock.Mock()

   #    # action
   #    returned_value = view.get_filtered_queryset(queryset, query)

   #    # assert
   #    self.assertTupleEqual((query,), queryset.filter.call_args[0])
   #    self.assertEqual(id(queryset.filter.return_value), id(returned_value))

   #def test_join_search_queries_should_create_sq_query_when_left_is_not_sq_instance_and_return_joined_left_and_right_queries(
   #        self):
   #    # setup
   #    view = BaseResultsView()
   #    left = '-keyword:'
   #    right = SQ(contains='something')

   #    # action
   #    returned_value = view.join_search_queries(left, right)

   #    # assert
   #    self.assertEqual(unicode(SQ(contains=Clean(left)) & right),
   #        unicode(returned_value))

   #def test_join_search_queries_should_create_sq_query_when_right_is_not_sq_instance_and_return_joined_left_and_right_queries(
   #        self):
   #    # setup
   #    view = BaseResultsView()
   #    left = SQ(contains='something')
   #    right = '-keyword:'

   #    # action
   #    returned_value = view.join_search_queries(left, right)

   #    # assert
   #    self.assertEqual(unicode(left & SQ(contains=Clean(right))),
   #        unicode(returned_value))

   #def test_join_search_queries_should_return_joined_left_and_right_queries_when_left_and_right_queries_are_already_sq_instances(
   #        self):
   #    # setup
   #    view = BaseResultsView()
   #    left = SQ(contains='something')
   #    right = SQ(contains='else')

   #    # action
   #    returned_value = view.join_search_queries(left, right)

   #    # assert
   #    self.assertEqual(unicode(left & right), unicode(returned_value))

   #def test_reduce_query_should_return_reduced_sq_query_upon_multiple_keywords(
   #        self):
   #    # setup
   #    view = BaseResultsView()
   #    keywords = ['something', 'else', 'foobar']

   #    # action
   #    returned_value = view.reduce_query(keywords)

   #    # assert
   #    self.assertEqual(unicode(SQ(contains=Clean(keywords[0])) \
   #        & SQ(contains=Clean(keywords[1])) \
   #        & SQ(contains=Clean(keywords[2]))), unicode(returned_value))

   #def test_reduce_query_should_return_create_sq_query_when_provided_with_only_one_keyword(
   #        self):
   #    # setup
   #    view = BaseResultsView()
   #    keywords = ['foobar']

   #    # action
   #    returned_value = view.reduce_query(keywords)

   #    # assert
   #    self.assertEqual(unicode(SQ(contains=Clean(keywords[0]))),
   #        unicode(returned_value))

   #@mock.patch('search.views.BaseResultsView.get_model')
   #@mock.patch('search.views.SearchQuerySet')
   #def test_get_queryset_should_return_unfiltered_search_query_set_for_model_when_no_keyword_no_locaton(
   #        self, sqs_class, get_model):
   #    # setup
   #    view = BaseResultsView()
   #    keywords = []
   #    location = ''
   #    models = sqs_class.return_value.models

   #    # action
   #    returned_value = view.get_queryset(keywords, location)

   #    # assert
   #    self.assertTupleEqual((get_model.return_value,), models.call_args[0])
   #    self.assertEqual(id(models.return_value.all.return_value),
   #        id(returned_value))

   #@mock.patch('search.views.BaseResultsView.get_filtered_queryset')
   #@mock.patch('search.views.BaseResultsView.reduce_query')
   #@mock.patch('search.views.BaseResultsView.get_model')
   #@mock.patch('search.views.SearchQuerySet')
   #def test_get_queryset_should_return_search_query_set_for_model_filtered_by_keywords_when_there_are_keywords(
   #        self, sqs_class, get_model, reduce_query, get_filtered_queryset):
   #    # setup
   #    view = BaseResultsView()
   #    keywords = ['k1', 'k2']
   #    location = ''
   #    models = sqs_class.return_value.models
   #    sqs = models.return_value.all.return_value

   #    # action
   #    returned_value = view.get_queryset(keywords, location)

   #    # assert
   #    self.assertTupleEqual((keywords,), reduce_query.call_args[0])
   #    self.assertTupleEqual((sqs, reduce_query.return_value,),
   #        get_filtered_queryset.call_args[0])
   #    self.assertEqual(id(get_filtered_queryset.return_value),
   #        id(returned_value))

   #@mock.patch('search.views.BaseResultsView.get_filtered_queryset')
   #@mock.patch('search.views.BaseResultsView.get_query_by_location')
   #@mock.patch('search.views.BaseResultsView.get_model')
   #@mock.patch('search.views.SearchQuerySet')
   #def test_get_queryset_should_return_search_query_set_for_model_filtered_by_location_when_there_are_locations(
   #        self, sqs_class, get_model, get_query_by_location,
   #        get_filtered_queryset):
   #    # setup
   #    view = BaseResultsView()
   #    keywords = []
   #    location = 'location1 location2'
   #    models = sqs_class.return_value.models
   #    sqs = models.return_value.all.return_value

   #    # action
   #    returned_value = view.get_queryset(keywords, location)

   #    # assert
   #    self.assertTupleEqual((location,), get_query_by_location.call_args[0])
   #    self.assertTupleEqual((sqs, get_query_by_location.return_value,),
   #        get_filtered_queryset.call_args[0])
   #    self.assertEqual(id(get_filtered_queryset.return_value),
   #        id(returned_value))

   #def test_get_object_list_should_return__empty_list_if_queryset_is_empty(
   #        self):
   #    # setup
   #    view = BaseResultsView()
   #    queryset = []

   #    # action
   #    returned_value = view.get_object_list(queryset)

   #    # assert
   #    self.assertListEqual([], returned_value)

   #def test_get_object_list_should_call_get_object_for_each_queryset_record_with_obj_best_match_and_if_match_was_saved_flag_as_args(
   #        self):
   #    # setup
   #    view = BaseResultsView()
   #    def get_object(*args):
   #        return args
   #    user_pk = 1
   #    request = mock.Mock()
   #    request.user.pk = user_pk
   #    view.request = request
   #    view.get_object = get_object
   #    r1 = mock.Mock()
   #    r1.matches = None
   #    r2 = mock.Mock()
   #    r2.matches = []
   #    r3 = mock.Mock()
   #    r3.user.pk = user_pk
   #    r3.matches = [str(user_pk)]
   #    queryset = mock.MagicMock()
   #    best_match = queryset.best_match.return_value
   #    queryset.__iter__.return_value = [r1, r2, r3]
   #    queryset.__len__.return_value = 3

   #    # action
   #    returned_value = view.get_object_list(queryset)

   #    # assert
   #    self.assertListEqual([
   #        (r1, best_match, False),
   #        (r2, best_match, False),
   #        (r3, best_match, True),],
   #        returned_value)

   #@mock.patch('search.views.HttpResponse')
   #@mock.patch('search.views.SearchFiltersForm')
   #@mock.patch('search.views.SearchForm')
   #def test_get_ajax_should_return_http_response_with_empty_json_results_when_no_keyword_no_location_and_was_search_button_clicked_is_false(
   #        self, search_form_class, search_filters_form_class,
   #        http_response_class):
   #    # setup
   #    view = BaseResultsView()
   #    request = mock.Mock()
   #    view.request = request
   #    search_form = search_form_class.return_value
   #    search_form.cleaned_data = {}

   #    # action
   #    returned_value = view.get_ajax(request)

   #    # assert
   #    self.assertDictEqual(dict(data=request.GET),
   #        search_form_class.call_args[1])
   #    self.assertEqual(1, search_form_class.call_count)
   #    self.assertTupleEqual(
   #        (('{}',), dict(content_type=view.get_content_type()),),
   #        http_response_class.call_args)
   #    self.assertEqual(id(http_response_class.return_value),
   #        id(returned_value))

   #@mock.patch('search.views.HttpResponse')
   #@mock.patch('search.views.json.dumps')
   #@mock.patch('search.views.BaseResultsView.get_context_data')
   #@mock.patch('search.views.BaseResultsView.get_object_list')
   #@mock.patch('search.views.BaseResultsView.get_queryset')
   #@mock.patch('search.views.SearchFiltersForm')
   #@mock.patch('search.views.SearchForm')
   #def test_get_ajax_should_return_http_response_with_json_results_when_keywords_are_available(
   #        self, search_form_class, search_filters_form_class, get_queryset,
   #        get_object_list, get_context_data, dumps, http_response_class):
   #    # setup
   #    view = BaseResultsView()
   #    request = mock.Mock()
   #    view.request = request
   #    keywords = '    k1    k2 k3   '
   #    cleaned_keywords = ['k1', 'k2', 'k3']
   #    search_form = search_form_class.return_value
   #    search_form.cleaned_data = dict(keywords=keywords)
   #    search_filters_form = search_filters_form_class.return_value
   #    search_filters_form.cleaned_data = {}
   #    get_queryset.return_value = []
   #    context = dict(paginator=mock.Mock(), page_obj=mock.Mock())
   #    get_context_data.return_value = context

   #    # action
   #    returned_value = view.get_ajax(request)

   #    # assert
   #    self.assertTupleEqual((cleaned_keywords, '',
   #        None, None, None, False, False, False), get_queryset.call_args[0])
   #    self.assertTupleEqual((get_queryset.return_value,),
   #        get_object_list.call_args[0])
   #    self.assertListEqual(get_queryset.return_value, view.object_list)
   #    self.assertEqual(1, get_context_data.call_count)
   #    self.assertTupleEqual((dict(
   #        object_list=get_object_list.return_value,
   #        num_pages=context['paginator'].num_pages,
   #        page_number=context['page_obj'].number),),
   #        dumps.call_args[0])
   #    self.assertTupleEqual(((dumps.return_value,),
   #        dict(content_type=view.get_content_type()),),
   #        http_response_class.call_args)
   #    self.assertEqual(id(http_response_class.return_value),
   #        id(returned_value))

   #def test_get_model_should_raise_not_implemented_error(self):
   #    # setup
   #    view = BaseResultsView()

   #    # action
   #    with self.assertRaises(NotImplementedError) as cm:
   #        view.get_model()

   #    # assert
   #    self.assertEqual(u'get_model() should be implemented',
   #        unicode(cm.exception))

   #def test_get_query_by_location_should_raise_not_implemented_error(self):
   #    # setup
   #    view = BaseResultsView()

   #    # action
   #    with self.assertRaises(NotImplementedError) as cm:
   #        view.get_query_by_location(mock.Mock())

   #    # assert
   #    self.assertEqual(u'get_query_by_location() should be implemented',
   #        unicode(cm.exception))

   #def test_get_object_should_raise_not_implemented_error(self):
   #    # setup
   #    view = BaseResultsView()

   #    # action
   #    with self.assertRaises(NotImplementedError) as cm:
   #        view.get_object(mock.Mock(), mock.Mock(), mock.Mock())

   #    # assert
   #    self.assertEqual(u'get_object() should be implemented',
   #        unicode(cm.exception))
    pass
