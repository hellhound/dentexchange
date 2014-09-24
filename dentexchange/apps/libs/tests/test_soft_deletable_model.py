# -*- coding:utf-8 -*-
import unittest
import mock

from ..models.soft_deletable import SoftDeletableModel, soft_delete


class SoftDeletableModelTestCase(unittest.TestCase):
    def setUp(self):
        self.show_active_only = SoftDeletableModel.show_active_only

    def tearDown(self):
        SoftDeletableModel.show_active_only = self.show_active_only

    def test_show_inactive_should_set_show_active_only_false(self):
        # action
        SoftDeletableModel.show_inactive()

        # assert
        self.assertFalse(SoftDeletableModel.show_active_only)

    def test_hide_inactive_should_set_show_active_only_true(self):
        # action
        SoftDeletableModel.hide_inactive()

        # assert
        self.assertTrue(SoftDeletableModel.show_active_only)

    def test_should_show_active_only_should_return_show_active_only(self):
        # setup
        SoftDeletableModel.show_active_only = False

        # assert
        self.assertFalse(SoftDeletableModel.should_show_active_only())

    @mock.patch('libs.models.soft_deletable.models.Model.delete')
    def test_delete_should_patch_collector_delete_and_call_super_delete(
            self, delete):
        # setup
        model = SoftDeletableModel()
        using = mock.Mock()

        # action
        model.delete(using=using)
        
        # assert
        self.assertDictEqual(dict(using=using), delete.call_args[1])
