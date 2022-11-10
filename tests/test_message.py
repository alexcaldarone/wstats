import unittest
from scripts.message import Message


class TestMessage(unittest.TestCase):

    def test_message(self):
        """
        Test against different input messages
        """

        with open('tests/data/chat_test_1.txt') as f:

            for l in f:

                message = Message(l)

                self.assertEqual(message.is_valid_message(l), True)
