# -*- coding:utf-8 -*-
import mock
import unittest

from ..models.soft_deletable import soft_delete, SoftDeletableModel


class SoftDeleteTestCase(unittest.TestCase):
    def test_soft_delete_should_call_qs_update_with_is_active_false_when_fast_deletes(
            self):
        # setup
        collector = self.get_collector()
        query = mock.Mock()
        collector.fast_deletes.append(query)

        # action
        soft_delete(collector)

        # assert
        self.assertDictEqual(dict(is_active=False), query.update.call_args[1])

    def test_soft_delete_should_set_is_active_false_for_each_instance_in_data_when_model_is_subclass_soft_deletable_model(
            self):
        # setup
        collector = self.get_collector()
        instance = mock.Mock()
        collector.data.update({SoftDeletableModel: [instance]})

        # action
        soft_delete(collector)
        
        # assert
        self.assertFalse(instance.is_active)
        self.assertEqual(1, instance.save.call_count)

    @mock.patch('libs.models.soft_deletable.Collector')
    def test_soft_delete_should_call_collector_delete_for_each_instance_in_data_when_model_is_not_subclass_soft_deletable_model(
            self, collector_class):
        # setup
        collector = self.get_collector()
        instance = mock.Mock()
        collector.data.update({object: [instance]})
        collaborator_collector = collector_class.return_value

        # action
        soft_delete(collector)

        # assert
        self.assertDictEqual(dict(using=None), collector_class.call_args[1])
        self.assertTupleEqual(([instance],),
            collaborator_collector.collect.call_args[0])
        self.assertEqual(1, collaborator_collector.delete.call_count)

    def get_collector(self):
        collector = mock.Mock()
        collector.fast_deletes = []
        collector.data = {}
        return collector
