import unittest
from scripts.analysis import Analysis
from scripts.message import Message

class TestAnalysis(unittest.TestCase):

    def setUp(self):
        # creating the attribute with the chat analyzed using the class
        self.analysis = Analysis()
        with open("tests/data/chat_test_1.txt", "r") as f:

            for i, line in enumerate(f):
                if i == 0:
                    continue
                message = Message(line)
                self.analysis.update_stats(message)
        self.analysis.calculate_avelength()
    
    def tearDown(self):
        self.analysis = None

    def test_chatDays(self):
        """
        Test that the days analyzed are the same and that the message count is the same
        """
        
        days_detected = self.analysis.STATS["Days"]
        days_correct = {
                "2022-03-29 00:00:00":7
            }

        self.assertDictEqual(days_correct, days_detected)

    def test_participants(self):
        """
        Testing that participants in the chat are the same
        """
        participants_detected = self.analysis["Participants"]
        participants_correct = set(["User1", "User2"])

        self.assertSetEqual(participants_correct, participants_detected)

    def test_time(self):
        """
        Testing that the times analyzed and the number of messages per hour are the same
        """
        times_detected = self.analysis["Time"]
        times_correct =  {
                "20":7
            }

        self.assertDictEqual(times_correct, times_detected)
        
    def test_chatWeekdays(self):
        """
        Test if the number of messaged sent on each weekday are correct
        """
        weekday_detected = self.analysis["Weekday"]
        weekday_correct = {
                "Monday": 0,
                "Tuesday": 7,
                "Wednesday": 0,
                "Thursday": 0,
                "Friday": 0,
                "Saturday": 0,
                "Sunday": 0
            }

        self.assertDictEqual(weekday_correct, weekday_detected)

    def test_startedChat(self):
        """
        Test if the number of chats started by each user is correct
        """
        chat_begins_detected = self.analysis["Started"]
        chat_begins_correct = {
                "User1":1
            }

        self.assertDictEqual(chat_begins_correct, chat_begins_detected)

    def test_averageLength(self):
        """
        Test that the average message length for each user is correct
        """
        average_length_detected = self.analysis["AveLength"]
        average_length_correct = {
                "User1":4.4,
                "User2":2.0
            }

        self.assertDictEqual(average_length_correct, average_length_detected)

    def test_numberMessagesPerUser(self):
        """
        Test if the message count by user is correct
        """
        message_by_user_detected = self.analysis["Number"]
        message_by_user_correct = {
                "User1":5,
                "User2":2
            }

        self.assertDictEqual(message_by_user_correct, message_by_user_detected)

    def test_typeOfMessage(self):
        """
        Test if the number of messages of each type is correct
        """
        type_detected = self.analysis["Type"]
        type_correct = {
                "Text":7
            }

        self.assertDictEqual(type_correct, type_detected)

if __name__ == '__main__':
    unittest.main()