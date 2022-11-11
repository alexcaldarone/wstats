import unittest
from datetime import datetime
from scripts.message import Message


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

        with open("tests/data/chat_test_1.txt", "r") as f:

            for l in f:
                
                message = Message(l)

                self.assertEqual(message.date, reference_date)
    

    def test_time(self):
        """
        Test the time attribute
        """
        time1 = "20:09"
        time2 = "20:10"
        i = 0 # line counter (to see what date I have to check)

        with open("tests/data/chat_test_1.txt", "r") as f:

            for l in f:
                
                message = Message(l)

                if i < 6:
                    self.assertEqual(message.time, time1)
                else:
                    self.assertEqual(message.time, time2)
                
                i += 1
    
    def test_author(self):
        """
        Test the author attribute
        """
        name1 = "User1"
        name2 = "User2"
        i = 0

        with open("tests/data/chat_test_1.txt", "r") as f:

            for l in f:
                
                message = Message(l)
                
                if i == 0:
                    # When i == 0, we are reading the first line which does not have an author
                    i += 1
                    continue
                elif i < 6:
                    self.assertEqual(message.author, name1)
                    i += 1
                else:
                    self.assertEqual(message.author, name2)
                    i += 1
            
                
        
    def test_type(self):
        """
        Test the type attribute
        """

        with open("tests/data/chat_test_1.txt", "r") as f:

            for l in f:
                
                message = Message(l)

                self.assertTrue(message.type, "Text")
    
    def test_weekday(self):
        """
        Test the weekday attribute
        """

        with open("tests/data/chat_test_1.txt", "r") as f:

            for l in f:
                
                message = Message(l)

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
        i = -1 # when i == -1 we are analyzing the first message, which has to be skipped

        with open("tests/data/chat_test_1.txt", "r") as f:

            for l in f:

                if i == -1:
                    i += 1
                    continue
                else:
                    message = Message(l.strip())
                    self.assertEqual(message.content, messages[i])
                    i += 1
        

if __name__ == '__main__':
    unittest.main()