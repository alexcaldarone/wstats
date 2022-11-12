import unittest
from scripts.message import Message


class TestMessage(unittest.TestCase):

    def test_message(self):
        """
        Test against different input messages
        """

        with open('tests/data/chat_test_1.txt') as f:

            for i, line in enumerate(f):

                message = Message(line)

                self.assertEqual(message.is_valid_message(line), True)

                if i in [x for x in range(1, 6)]:
                    self.assertEqual(message.author == 'User1', True)

                if i in [x for x in range(6, 8)]:
                    self.assertEqual(message.author == 'User2', True)
