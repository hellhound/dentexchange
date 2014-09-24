# -coding:utf-8 -*-
import unittest
import mock

from ..forms import ResumeForm
from .. import constants


class ResumeFormTestCase(unittest.TestCase):
    @mock.patch('employee.forms.QuotaValidator')
    @mock.patch('employee.forms.forms.ModelForm.__init__')
    def test_init_should_set_cv_file_field_validators_to_validated_files_quaota_validator(
            self, __init__, validator_class):
        # setup
        __init__.return_value = None
        ResumeForm.fields = dict(cv_file=mock.Mock())

        # action
        form = ResumeForm()

        # asert
        self.assertDictEqual(
            dict(max_usage=constants.RESUME_CV_FILE_CONTENT_TYPES),
            validator_class.call_args[1])
        self.assertListEqual([[validator_class.return_value]],
            [form.fields['cv_file'].validators])
