# -*- coding:utf-8 -*-
import unittest
import mock

from ..tasks import send_confirmation
from .. import strings, constants


class SendConfirmationTestCase(unittest.TestCase):
    @mock.patch('authentication.tasks.EmailMultiAlternatives')
    @mock.patch('authentication.tasks.render_to_string_text')
    @mock.patch('authentication.tasks.render_to_string_html')
    @mock.patch('authentication.tasks.RecoveryToken')
    @mock.patch('authentication.tasks.User')
    def test_send_confirmation_should_grab_user_info_build_email_message_and_call_send(
            self, user_class, recovery_token_class,
            render_to_string_html, render_to_string_text,
            email_multi_alternatives_class):
        # setup
        host = 'somehost'
        email = 'an@example.com'
        user = user_class.objects.get(email=email)
        token = recovery_token_class.objects.create.return_value
        html = render_to_string_html.return_value
        body = render_to_string_text.return_value
        msg = email_multi_alternatives_class.return_value

        # action
        send_confirmation(host, email)

        # assert
        self.assertDictEqual(dict(email=email),
            user_class.objects.get.call_args[1])
        self.assertDictEqual(dict(user=user),
            recovery_token_class.objects.create.call_args[1])
        self.assertTupleEqual(('authentication/mail/email_confirmation.html',
            dict(token=token, http_host=host)),
            render_to_string_html.call_args[0])
        self.assertTupleEqual(('authentication/mail/email_confirmation.txt',
            dict(token=token, http_host=host)),
            render_to_string_text.call_args[0])
        self.assertTupleEqual((strings.SEND_CONFIRMATION_SUBJECT, body,
            constants.FROM_PASSWORD_RECOVERY_EMAIL, [email]),
            email_multi_alternatives_class.call_args[0])
        self.assertTupleEqual((html, 'text/html'),
            msg.attach_alternative.call_args[0])
        self.assertEqual(1, msg.send.call_count)
