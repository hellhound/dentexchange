# -*- coding:utf-8 -*-
import unittest
import mock

from ..models import JobPosting


class JobPostingTestCase(unittest.TestCase):
    def test_unicode_should_return_position_name(self):
        # setup
        model = JobPosting()
        model.position_name = 'Position Name'

        # action
        email = unicode(model)

        # assert
        self.assertEqual(model.position_name, email)
