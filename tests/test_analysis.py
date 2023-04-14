import unittest
import pandas as pd
import numpy as np
from scripts.analysis import Analysis
from scripts.message import Message
from collections import Counter

class TestAnalysis(unittest.TestCase):

    def setUp(self):
        # creating the attribute with the chat analyzed using the class
        with open("tests/data/chat_test_1_ref", "r") as f:
            self.df = pd.read_csv(f, index_col = 0)
    
    def tearDown(self):
        self.df = None
    
    def test_DataframeCreation(self):
        """
        Test that the dataframe is created correctly
        """
        analysis = Analysis()
        last_message_analyzed = None
        with open("tests/data/chat_test_1.txt", "r") as f:
            
            for i, line in enumerate(f):
                if i == 0:
                    continue

                if Message.is_valid_message(Message, line):  # check if valid message
                    message = Message(line.strip())
                    last_message_analyzed = analysis.update_list(message)
                else:
                    # if it isn't a valid message it's continuation of previous message
                    if last_message_analyzed:
                        analysis.update_last_message(line)
        
        analysis.generate_dataframe()
        
        # testing that the stats attribute is actually a dataframe
        self.assertEqual(isinstance(analysis.stats, pd.DataFrame), True)

    def test_messagesPerDay(self):
        """
        Test that the days analyzed are the same and that the message count is the same
        """
        reference = pd.Series(data=[8, 9, 9, 9, 7],
                              index = ["2022-03-29", "2022-03-31", "2022-04-10",
                                       "2022-04-15", "2022-04-21"])
        
        analysis = Analysis()
        analysis.stats = self.df

        messages_day = analysis.get_messages_per_day()

        self.assertEqual(reference.equals(messages_day), True)

    def test_participants(self):
        """
        Testing that participants in the chat are the same
        """
        reference = np.array(["User1", "User2"], dtype=str)
        
        analysis = Analysis()
        analysis.stats = self.df

        participants = analysis.get_chat_participants()

        self.assertEqual(np.array_equal(reference, participants), True)

    def test_time(self):
        """
        Testing that the number of messages sent per hour
        """
        reference_dict = {
            0: 0,
            1: 0,
            2: 0,
            3: 0,
            4: 0,
            5: 0,
            6: 0,
            7: 0,
            8: 0,
            9: 0,
            10: 9,
            11: 9,
            12: 0,
            13: 0,
            14: 0,
            15: 0,
            16: 9,
            17: 0,
            18: 0,
            19: 7,
            20: 8,
            21: 0,
            22: 0,
            23: 0
        }
        reference = pd.Series(reference_dict)
        
        analysis = Analysis()
        analysis.stats = self.df

        messages_hour = analysis.get_messages_by_hour()

        self.assertEqual(reference.equals(messages_hour), True)

    def test_chatWeekdays(self):
        """
        Test if the number of messaged sent on each weekday are correct
        """
        reference_dict = {
            "Monday": 0,
            "Tuesday": 8,
            "Wednesday": 0,
            "Thursday": 16,
            "Friday": 9,
            "Saturday": 0,
            "Sunday": 9
        }
        reference = pd.Series(reference_dict)
        
        analysis = Analysis()
        analysis.stats = self.df

        messages_weekday = analysis.get_messages_by_weekday()

        self.assertEqual(reference.equals(messages_weekday), True)

    def test_startedChat(self):
        """
        Test if the number of chats started by each user is correct
        """
        reference = pd.Series(data = [5], index=["User1"])
        
        analysis = Analysis()
        analysis.stats = self.df

        chats_started = analysis.chats_started_by_user()

        self.assertEqual(reference.equals(chats_started), True)

    def test_averageLength(self):
        """
        Test that the average message length for each user is correct
        """
        reference = pd.Series(data=[8.695652173913043, 8.894736842105264], index=["User1", "User2"])

        analysis = Analysis()
        analysis.stats = self.df

        average_length = analysis.average_message_length_by_user()

        self.assertEqual(reference.equals(average_length), True)

    def test_numberMessagesPerUser(self):
        """
        Test if the message count by user is correct
        """
        reference = pd.Series(data=[23, 19], index = ["User1", "User2"])
        
        analysis = Analysis()
        analysis.stats = self.df

        messages_per_user = analysis.get_messages_per_user()

        self.assertEqual(reference.equals(messages_per_user), True)

    def test_typeOfMessage(self):
        """
        Test if the number of messages of each type is correct
        """
        reference = pd.Series(data=[40, 2, 0], index=["Text", "Media", "Link"])

        analysis = Analysis()
        analysis.stats = self.df

        messages_type = analysis.get_messages_by_type()

        self.assertEqual(reference.equals(messages_type), True)

    # add test for most common words per user

if __name__ == '__main__':
    unittest.main()