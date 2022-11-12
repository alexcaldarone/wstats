import unittest
from datetime import datetime
from scripts.message import Message


class TestMessage(unittest.TestCase):

    def test_is_valid_message(self):
        """
        Test against different input messages
        """

        with open('tests/data/chat_test_1.txt', 'r') as f:

            for i, line in enumerate(f):

                message = Message(line)

                self.assertEqual(message.is_valid_message(line), True)

    def test_date(self):
        """
        Tests that the date attribute of the chat messages is created correctly
        """
        reference_date = datetime(year=2022, month=3, day=29)

        with open('tests/data/chat_test_1.txt', 'r') as f:

            for i, line in enumerate(f):

                message = Message(line)

                self.assertEqual(message.date, reference_date)

    def test_time(self):
        """
        Test the time attribute
        """
        time1 = "20:09"
        time2 = "20:10"
        time3 = "21:10"

        with open('tests/data/chat_test_1.txt', 'r') as f:

            for i, line in enumerate(f):

                message = Message(line)

                if i < 6:
                    self.assertEqual(message.time, time1)
                    self.assertEqual(message.time == time3, False)
                else:
                    self.assertEqual(message.time, time2)

    def test_author(self):
        """
        Test the author attribute
        """

        with open('tests/data/chat_test_1.txt', 'r') as f:

            for i, line in enumerate(f):

                message = Message(line)

                if i in [x for x in range(1, 6)]:
                    self.assertEqual(message.author == 'User1', True)
                    self.assertEqual(message.author == 'User2', False)

                if i in [x for x in range(6, 8)]:
                    self.assertEqual(message.author == 'User2', True)
                    self.assertEqual(message.author == 'User1', False)

    def test_type(self):
        """
        Test the type attribute
        """

        with open('tests/data/chat_test_1.txt', 'r') as f:

            for i, line in enumerate(f):

                message = Message(line)

                self.assertTrue(message.type, "Text")

    def test_weekday(self):
        """
        Test the weekday attribute
        """

        with open('tests/data/chat_test_1.txt', 'r') as f:

            for i, line in enumerate(f):

                message = Message(line)

                self.assertTrue(message.weekday, "Tuesday")

    def test_content(self):
        """
        Test the content attribute

        We need to verify that for every message object the content attribute is equal to the text contained in the file
        """
        messages = [
            " Hello,",
            " I am here",
            " This is a line with comma,",
            " Another one with multiple commas,,,,",
            " ,casual commas,,",
            " Ok",
            " ."
        ]

        with open('tests/data/chat_test_1.txt', 'r') as f:

            for i, line in enumerate(f.readlines()[1:]):

                message = Message(line.strip())
                self.assertEqual(message.content, messages[i])


if __name__ == '__main__':
    unittest.main()
