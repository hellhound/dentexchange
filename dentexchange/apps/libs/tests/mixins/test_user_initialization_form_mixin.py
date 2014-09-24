# -*- coding:utf-8 -*-
import unittest
import mock

from ...mixins.forms import UserInitializationFormMixin


class UserInitializationFormMixinTestCase(unittest.TestCase):
    def test_init_should_initialize_user_ivar_with_user_arg(self):
        # setup
        user = mock.Mock()

        # action
        mixin = UserInitializationFormMixin(user=user)

        # assert
        self.assertEqual(id(user), id(mixin.user))

    def test_init_should_initialize_user_with_none_without_user_arg(self):
        # setup and action
        mixin = UserInitializationFormMixin()

        # assert
        self.assertIsNone(mixin.user)

    @mock.patch('libs.mixins.forms.Mixin.base_impl')
    def test_save_should_call_super_with_commit_false_save_instance_and_return_instance_with_user(
            self, base_impl):
        # setup
        user = mock.Mock()
        mixin = UserInitializationFormMixin(user=user)
        mixin.user = user
        save = base_impl.return_value.save
        instance = save.return_value

        # action
        returned_value = mixin.save()

        # assert
        self.assertDictEqual(dict(commit=False), save.call_args[1])
        self.assertEqual(id(user), id(instance.user))
        self.assertEqual(id(instance), id(returned_value))
        self.assertEqual(1, instance.save.call_count)

    @mock.patch('libs.mixins.forms.Mixin.base_impl')
    def test_shouldnt_call_instance_save_when_commit_false(self, base_impl):
        # setup
        mixin = UserInitializationFormMixin()
        instance = base_impl.return_value.save.return_value

        # action
        mixin.save(commit=False)

        # assert
        self.assertEqual(0, instance.save.call_count)
