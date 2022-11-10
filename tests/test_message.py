import unittest
from datetime import datetime
from scripts.message import Message

'''
To add:
    - Test creation of date attribute
    - test time attribute
    - test author
    - test content
    - test type
    - test weekday
'''

class TestMessage(unittest.TestCase):

    def test_valid_message(self):
        """
        Test against different input messages
        """

        with open('tests/data/chat_test_1.txt', 'r') as f:

            for l in f:

                message = Message(l)

                self.assertEqual(message.is_valid_message(l), True)
    
    
    def test_date(self):
        """
        Tests that the date attribute of the chat messages is created correctly
        """
        reference_date = datetime(year = 2022, month = 3, day = 29)

        with open('tests/data/chat_test_1.txt', 'r') as f:

            for l in f:
                
                message = Message(l)

                self.assertEqual(message.date, reference_date)

if __name__ == '__main__':
    unittest.main()