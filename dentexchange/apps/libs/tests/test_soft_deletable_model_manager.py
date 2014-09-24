# -*- coding:utf-8 -*-
import mock
import unittest

from django.db import models

from ..models.soft_deletable import SoftDeletableModelManager


class SoftDeletableModelManagerTestCase(unittest.TestCase):
    @mock.patch('libs.models.soft_deletable.QuerySetProxy')
    @mock.patch('libs.models.soft_deletable.models.Manager.get_queryset')
    def test_get_queryset_should_return_unfiltered_query_set_proxy(self,
            get_queryset, query_set_proxy_class):
        # setup
        manager = self.get_model().objects
        manager.model = mock.Mock()
        manager.model.should_show_active_only.return_value = False
        query = get_queryset.return_value

        # action
        returned_value = manager.get_queryset()

        # assert
        self.assertTupleEqual((query,), query_set_proxy_class.call_args[0])
        self.assertEqual(id(query_set_proxy_class.return_value),
            id(returned_value))

    @mock.patch('libs.models.soft_deletable.QuerySetProxy')
    @mock.patch('libs.models.soft_deletable.models.Manager.get_queryset')
    def test_get_queryset_should_return_filtered_query_set_proxy_by_is_active_true(
            self, get_queryset, query_set_proxy_class):
        # setup
        manager = self.get_model().objects
        manager.model = mock.Mock()
        manager.model.should_show_active_only.return_value = True
        query = get_queryset.return_value

        # action
        returned_value = manager.get_queryset()

        # assert
        self.assertDictEqual(dict(is_active=True), query.filter.call_args[1])
        self.assertTupleEqual((query.filter.return_value,),
            query_set_proxy_class.call_args[0])
        self.assertEqual(id(query_set_proxy_class.return_value),
            id(returned_value))

    def get_model(self):
        class Model(models.Model):
            objects = SoftDeletableModelManager()

        return Model
