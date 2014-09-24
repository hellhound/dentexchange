# -*- coding:utf-8 -*-
import mock
import unittest


from ...auth.builder import UserFactory


class UserFactoryTestCase(unittest.TestCase):
    def setUp(self):
        self.get_username_from_email = UserFactory.get_username_from_email

    def tearDown(self):
        UserFactory.get_username_from_email = self.get_username_from_email

    @mock.patch('libs.auth.builder.User.objects.filter')
    def test_user_exists_should_return_true_if_hashed_email_exists(
            self, user_filter):
        # setup
        email = 'an@example.com'
        user_filter.return_value.count.return_value = 1
        UserFactory.get_username_from_email = mock.Mock()

        # action
        returned_value = UserFactory.user_exists(email)

        # assert
        self.assertTupleEqual((email,),
            UserFactory.get_username_from_email.call_args[0])
        self.assertDictEqual(
            dict(username=UserFactory.get_username_from_email(email)),
            user_filter.call_args[1])
        self.assertTrue(returned_value)

    @mock.patch('libs.auth.builder.User.objects.filter')
    def test_user_exists_should_return_false_if_hashed_email_doesnt_exists(
            self, user_filter):
        # setup
        email = 'an@example.com'
        user_filter.return_value.count.return_value = 0
        UserFactory.get_username_from_email = mock.Mock()

        # action
        returned_value = UserFactory.user_exists(email)

        # assert
        self.assertTupleEqual((email,),
            UserFactory.get_username_from_email.call_args[0])
        self.assertDictEqual(
            dict(username=UserFactory.get_username_from_email(email)),
            user_filter.call_args[1])
        self.assertFalse(returned_value)

    @mock.patch('libs.auth.builder.User')
    def test_create_user_should_hash_email_use_it_as_username_set_password_and_returned_saved_user(
            self, user_class):
        # setup
        email = 'an@example.com'
        password = 'password'
        UserFactory.get_username_from_email = mock.Mock()

        # action
        returned_value = UserFactory.create_user(email, password)

        # assert
        self.assertTupleEqual((email,),
            UserFactory.get_username_from_email.call_args[0])
        self.assertDictEqual(
            dict(username=UserFactory.get_username_from_email.return_value,
            email=email),
            user_class.call_args[1])
        self.assertTupleEqual((password,),
            user_class.return_value.set_password.call_args[0])
        self.assertEqual(1, user_class.return_value.save.call_count)
        self.assertEqual(id(user_class.return_value), id(returned_value))

    @mock.patch('libs.auth.builder.random.randint')
    @mock.patch('libs.auth.builder.hashlib.sha1')
    @mock.patch('libs.auth.builder.salt_b64encode')
    @mock.patch('libs.auth.builder.sha1_b64encode')
    def test_get_username_from_email_should_hash_and_normalize_email(
            self, sha1_b64encode, salt_b64encode, sha1, randint):
        # setup
        email = 'a@verylargeemailexample.com'
        normalized_email = 'a_verylargeemailexample.com'
        randint.return_value = 10
        salt_b64encode.return_value = 'abcdefghijklmnopqrstuvwxyz0123456789ABCD'
        sha1_b64encode.return_value = 'abcdefghijklmnopqrstuvwxyz0123456789ABCD'

        # action
        returned_value = UserFactory.get_username_from_email(email)

        # assert
        self.assertTupleEqual((email,), sha1.call_args[0])
        self.assertTupleEqual((sha1.return_value.digest.return_value,),
            sha1_b64encode.call_args[0])
        self.assertTupleEqual((0, 2**64,), randint.call_args[0])
        self.assertTupleEqual(('10',), salt_b64encode.call_args[0])
        self.assertEqual(
            (normalized_email[:10] + salt_b64encode.return_value[:-10] \
            + salt_b64encode.return_value)[:30], returned_value)
