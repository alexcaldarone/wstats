from scripts.message import Message
import nltk
import pandas as pd

class Analysis:
    """

    Existing stats i need to re-implement:
        - ---participants
        - number of messages per hour
        - how many chats were started by each user
        - average length of messages
        - ---number of messages per day
        - number of messages by each message type
        - number of messages for each weekday

    Extra features to add:
        - frequency of most used words by each user (nltk.freqDist)
        - possibility to choose a word and see how many times it has been used (globally and for each user)
        - chat and user wordcloud
        - sentiment analysis

    A class to contain the statistics of a whatsapp chat

    Attributes
    --------------------
        self.STATS: dict
            Dictionary containing the statistics of the chat
        self.last_date: str
            Saves the date of the last message analyzed (used to determine who started a conversation)
    """

    def __init__(self):
        """Constructor"""
        # what i want to do is store the message objects in a list and then create a dataframe
        # once i have the dataframe i can do nlp on it
        self.__tempList = []
    
    def update_list(self, message: Message):
        self.__tempList.append(message.to_list())

        return self.__tempList[-1] # returns the last message added
    
    def update_last_message(self, line: str):
        self.__tempList[-1].content += line

    def generate_dataframe(self):
        self.stats = pd.DataFrame(self.__tempList, 
            columns= ["Date", "Time", "Author", "Content", "Type", "Weekday"])
    
    def get_messages_per_day_per_user(self): # counts the number of messages per day
        return self.stats.groupby(["Date", "Author"])["Content"].count()
    
    def get_messages_per_user(self):
        return self.stats.groupby("Author")["Content"].count()

    def get_messages_per_day(self):
        return self.stats.groupby("Date")["Content"].count()

    def get_messages_by_type(self):
        return self.stats.groupby("Type")["Content"].count()

    def get_messages_by_weekday(self):
        return self.stats.groupby("Weekday")["Content"].count()

    def get_messages_by_hour(self):
        return self.stats.groupby("Time")["Content"].count()

    def get_messages_by_hour_by_user(self):
        pass

    def average_message_length_by_user(self):
        self.stats["message_length"] = self.stats["Content"].apply(lambda x: len(x.split()))
        
        return self.stats.groupby("Author")["message_length"].mean()

    def chats_started_by_user(self):
        pass

    def get_chat_participants(self):
        return self.stats["Author"].unique()