import unittest
from datetime import datetime
from scripts.message import Message
import pandas as pd

class TestMessage(unittest.TestCase):

    def setUp(self):

        with open("tests/data/chat_test_1_ref", "r") as f:
            self.reference_df = pd.read_csv(f)

    def tearDown(self):
        self.reference_df = None

    def test_is_valid_message(self):
        """
        Test against different input messages
        """

        with open('tests/data/chat_test_1.txt', 'r') as f:

            for i, line in enumerate(f):
                
                if i == 0:
                    continue

                message = Message(line)

                self.assertEqual(message.is_valid_message(line), True)

    def test_date(self):
        """
        Tests that the date attribute of the chat messages is created correctly
        """
        reference_dates = self.reference_df["Date"]

        with open("tests/data/chat_test_1.txt", "r") as f:
        
            for i, line in enumerate(f):
                if i == 0:
                    continue
                
                message = Message(line)

                self.assertEqual(str(message.date)[:-9], reference_dates[i-1])

    def test_time(self):
        """
        Test the time attribute
        """
        reference_times = self.reference_df["Time"]

        with open("tests/data/chat_test_1.txt", "r") as f:

            for i, line in enumerate(f):
                if i == 0:
                    continue

                message = Message(line)

                self.assertEqual(message.time, reference_times[i-1])

    def test_author(self):
        """
        Test the author attribute
        """
        reference_authors = self.reference_df["Author"]

        with open("tests/data/chat_test_1.txt", "r") as f:

            for i, line in enumerate(f):
                if i == 0:
                    continue

                message = Message(line)

                self.assertEqual(message.author, reference_authors[i-1])

    def test_type(self):
        """
        Test the type attribute
        """
        reference_types = self.reference_df["Type"]

        with open("tests/data/chat_test_1.txt", "r") as f:

            for i, line in enumerate(f):
                if i == 0:
                    continue

                message = Message(line)

                self.assertEqual(message.type, reference_types[i-1])

    def test_weekday(self):
        """
        Test the weekday attribute
        """
        reference_weekdays = self.reference_df["Weekday"]

        with open("tests/data/chat_test_1.txt", "r") as f:

            for i, line in enumerate(f):
                if i == 0:
                    continue

                message = Message(line)

                self.assertEqual(message.weekday, reference_weekdays[i-1])

    def test_content(self):
        """
        Test the content attribute

        We need to verify that for every message object the content attribute is equal to the text contained in the file
        """
        reference_content = self.reference_df["Content"]

        with open("tests/data/chat_test_1.txt", "r") as f:

            for i, line in enumerate(f):
                if i == 0:
                    continue

                message = Message(line)

                self.assertEqual(message.content.strip(), reference_content[i-1])


if __name__ == '__main__':
    unittest.main()
