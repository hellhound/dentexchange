# -*- coding:utf-8- -*-
import unittest
import mock

from ..tasks import send_welcome_message
from .. import strings, constants


class SendWelcomeMessageTestCase(unittest.TestCase):
    @mock.patch('registration.tasks.EmailMultiAlternatives')
    @mock.patch('registration.tasks.render_to_string_text')
    @mock.patch('registration.tasks.render_to_string_html')
    @mock.patch('registration.tasks.User')
    def test_send_confirmation_should_grab_user_info_build_email_message_and_call_send(
            self, user_class, render_to_string_html, render_to_string_text,
            email_multi_alternatives_class):
        # setup
        host = 'somehost'
        email = 'an@example.com'
        user = user_class.objects.get(email=email)
        html = render_to_string_html.return_value
        body = render_to_string_text.return_value
        msg = email_multi_alternatives_class.return_value

        # action
        send_welcome_message(host, email)

        # assert
        self.assertDictEqual(dict(email=email),
            user_class.objects.get.call_args[1])
        self.assertTupleEqual(('registration/mail/welcome.html',
            dict(user=user, http_host=host)),
            render_to_string_html.call_args[0])
        self.assertTupleEqual(('registration/mail/welcome.txt',
            dict(user=user, http_host=host)),
            render_to_string_text.call_args[0])
        self.assertTupleEqual((strings.SEND_WELCOME_MESSAGE, body,
            constants.FROM_WELCOME_EMAIL, [email]),
            email_multi_alternatives_class.call_args[0])
        self.assertTupleEqual((html, 'text/html'),
            msg.attach_alternative.call_args[0])
        self.assertEqual(1, msg.send.call_count)
