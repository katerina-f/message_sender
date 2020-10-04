# internal modules
from datetime import datetime
import json
from unittest import TestCase, main
from unittest.mock import Mock, MagicMock, patch, call, create_autospec

# project modules
from app.utils import Validator

from .test_data import *


class TestValidator(TestCase):

    def setUp(self):
        self.validator = Validator()

    @patch("app.utils.Validator.validate_recipient")
    @patch("app.utils.Validator.validate_recipients")
    def test_validate(self, validate_recipients, validate_recipient):
        self.assertEqual(valide_message, self.validator.validate(valide_message))
        validate_recipients.assert_called_once_with(valide_recipients)

        for message in wrong_messages:
            with self.subTest(msg=f"test with {message}"):
                with self.assertRaises((TypeError, ValueError)):
                    self.validator.validate(message)

    def test_validate_recipients(self):
        with self.assertRaises(TypeError):
            self.validator.validate_recipients(wrong_recipients)
        self.assertEqual(self.validator.validate_recipients(valide_recipients), valide_recipients)

    def test_validate_recipient(self):
        for rec in wrong_recipients:
            with self.subTest(msg=f"test with {rec}"):
                with self.assertRaises(TypeError):
                    self.validator.validate_recipient(rec)

        for rec in valide_recipients:
            with self.subTest(msg=f"test with {rec}"):
                self.assertEqual(self.validator.validate_recipient(rec), rec)

    def test_validate_send_date(self):
        with self.assertRaises((TypeError, ValueError)):
            self.validator.validate_send_at(wrong_send_date)

        self.assertEqual(self.validator.validate_send_at(valide_send_date), valide_send_date)

if __name__ == "__main__":
    main()
