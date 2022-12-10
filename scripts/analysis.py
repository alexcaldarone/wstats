from scripts.message import Message
import nltk
import pandas as pd

class Analysis:
    """

    Existing stats i need to re-implement:
        - ---participants
        - ---number of messages per hour
        - ---how many chats were started by each user
        - ---average length of messages
        - ---number of messages per day
        - ---number of messages by each message type
        - ---number of messages for each weekday

    Extra features to add:
        - frequency of most used words by each user (nltk.freqDist)
        - possibility to choose a word and see how many times it has been used (globally and for each user)
        - chat and user wordcloud
        - sentiment analysis

    A class to contain the statistics of a whatsapp chat

    Attributes
    --------------------
        self.stats: pd.DataFrame
            Dataframe containing the chat's data
    """

    def __init__(self):
        """Constructor"""
        self.__tempList = []
        self.stats = None

    
    def update_list(self, message: Message):
        """
        Updates the list containing the chat's messages.
        To store each message the Message object is converted to a list.

        Parameters
        --------------------
            line: str
                Line to be analyzed

        Returns
        --------------------
            Last element of the list 
        """
        self.__tempList.append(message.to_list())

        return self.__tempList[-1] # returns the last message added


    def update_last_message(self, line: str):
        """
        Updates the content of the last chat message analyzed.
        This is necessary when a new line does not corrispond with a new message.
        In this case we add the line to the content attribute of the last message analyzed.

        Parameters
        --------------------
            line: str
                Line to be analyzed
        """
        self.__tempList[-1].content += line


    def generate_dataframe(self):
        """
        Generates the dataframe containing the chat's data.
        This is done by converting the previously created list to a dataframe.
        """
        # check to avoid creating an empty dataframe
        if len(self.__tempList) == 0:
            raise Exception("Cannot create DataFrame without chat data")
        
        self.stats = pd.DataFrame(self.__tempList, 
            columns= ["Date", "Time", "Author", "Content", "Type", "Weekday"])


    def get_messages_per_day_per_user(self):
        """
        Counts the number of messages sent each day by each user

        Returns
        --------------------
            pandas.core.series.Series
                Pandas Series containing the number of messages per day per user.
        """
        return self.stats.groupby(["Date", "Author"])["Content"].count()


    def get_messages_per_user(self):
        """
        Counts the total number of messages sent by each user

        Returns
        --------------------
            pandas.core.series.Series
                Pandas Series containing the number of messages sent per user.
        """
        return self.stats.groupby("Author")["Content"].count()


    def get_messages_per_day(self):
        """
        Counts the number of messages sent each day (by all users)

        Returns
        --------------------
            pandas.core.series.Series
                Pandas Series containing the number of messages sent per day.
        """
        return self.stats.groupby("Date")["Content"].count()


    def get_messages_by_type(self):
        """
        Counts the number of messages for each message type (text, media, link)

        Returns
        --------------------
            pandas.core.series.Series
                Pandas Series containing the number of messages for each type
        """
        # should I add the types that were not present in the chat with count = 0?
        return self.stats.groupby("Type")["Content"].count()


    def get_messages_by_weekday(self):
        """
        Counts the number of messages sent on each weekday

        Returns
        --------------------
            pandas.core.series.Series
                Pandas Series containing the number of messages on each weekday
        """
        # should I add the weekdays that were not present in the chat with count = 0?
        return self.stats.groupby("Weekday")["Content"].count()


    def get_messages_by_hour(self):
        """
        Counts the number of messages sent each hour

        Returns
        --------------------
            pandas.core.series.Series
                Pandas Series containing the number of messages each hour
        """
        # should I add the hours that were not present in the chat with count = 0?
        self.stats["hour"] = self.stats["Time"].apply(lambda x: x[0:2])
        return self.stats.groupby("hour")["Content"].count()


    def get_messages_by_hour_by_user(self):
        """
        Counts the number of messages sent each hour by each user

        Returns
        --------------------
            pandas.core.series.Series
                Pandas Series containing the number of messages each hour by each user
        """
        # should I add the hours that were not present in the chat with count = 0?
        return self.stats.groupby(["hour", "Author"]).count()


    def average_message_length_by_user(self):
        """
        Counts the average length of each user's messagges

        Returns
        --------------------
            pandas.core.series.Series
                Pandas Series containing the average length of each user
        """
        self.stats["message_length"] = self.stats["Content"].apply(lambda x: len(x.split()))
        
        return self.stats.groupby("Author")["message_length"].mean()


    def chats_started_by_user(self): # how to do better ?
        """
        Counts the number of conversations started by each user

        Returns
        --------------------
            pandas.core.series.Series
                Pandas Series containing the number of conversations started by each user
        """
        # should I add the hours that were not present in the chat with count = 0?
        res = []
        unique_date = self.stats["Date"].unique()

        for date in unique_date:
            messages = self.stats[self.stats["Date"] == date].iloc[0]
            res.append([messages["Date"], messages["Author"]])
        
        chat_starters = pd.DataFrame(res, columns=["Date", "Author"])

        return chat_starters.groupby("Author")["Date"].count()


    def get_chat_participants(self):
        """
        Returns the participants in the chat

        Returns
        --------------------
            numpy.ndarray
                Participants in the chat
        """
        return self.stats["Author"].unique()