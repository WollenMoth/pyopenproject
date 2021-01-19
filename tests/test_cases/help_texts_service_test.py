import json

from business.exception.business_error import BusinessError
from model.help_text import HelpText
from tests.test_cases.openproject_test_case import OpenProjectTestCase


class HelpTextsServiceTestCase(OpenProjectTestCase):

    def setUp(self):
        super().setUp()
        self.helpSer = self.factory.get_help_texts_service()
        with open('../data/help_text.json') as f:
            self.help_text = HelpText(json.load(f))

    def test_find(self):
        # There's no help text --> Exception
        with self.assertRaises(BusinessError):
            self.assertIsNotNone(self.helpSer.find(self.help_text))

    def test_find_all(self):
        self.assertIsNotNone(self.helpSer.find_all())
