from scripts.message import Message
import nltk
import pandas as pd
from collections import Counter

# nltk.download("punkt")
# move the installation of these libraries into setup.py?

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
        self.stats = None
        self.__tempList = []
        self.__textSubDdf = None
    
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
        # necessary because of conversion of the message object to list
        CONTENT_INDEX = 3 
        self.__tempList[-1][CONTENT_INDEX] += line


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
    
    #
    # CHAT SUMMRY METHODS
    #

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
        def get_freq(series, type):
            """
            Returns the number of messages on a given weekday if there were any, 
            zero otherwise.
            Used to construct the pd.Series object containing all the frequencies
            """
            if type not in series.index:
                return 0
            return series[type]
        
        types_available = ["Text", "Media", "Link"]
        observed = self.stats.groupby("Type")["Content"].count()
        res = [get_freq(observed, message_type) for message_type in types_available]

        return pd.Series(data=res, index=types_available)


    def get_messages_by_weekday(self):
        """
        Counts the number of messages sent on each weekday

        Returns
        --------------------
            pandas.core.series.Series
                Pandas Series containing the number of messages on each weekday
        """
        def get_freq(series, day):
            """
            Returns the number of messages on a given weekday if there were any, 
            zero otherwise.
            Used to construct the pd.Series object containing all the frequencies
            """
            if day not in series.index:
                return 0
            return series[day]
        
        weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

        observed = self.stats.groupby("Weekday")["Content"].count()
        res = [get_freq(observed, day) for day in weekdays]

        return pd.Series(data=res, index=weekdays, name="messages_per_weekday") 


    def get_messages_by_hour(self):
        """
        Counts the number of messages sent each hour

        Returns
        --------------------
            pandas.core.series.Series
                Pandas Series containing the number of messages each hour
        """
        def get_freq(series, hour):
            """
            Returns the number of messages at a given hour if there were any, 
            zero otherwise.
            Used to construct the pd.Series object containing all the frequencies
            """
            if hour not in series.index:
                return 0
            return series[hour]
        
        self.stats["hour"] = self.stats["Time"].apply(lambda x: x[0:2])
        observed = self.stats.groupby("hour")["Content"].count() # surflous ?
        res = [get_freq(observed, str(i)) for i in range(0, 24)]
        
        return pd.Series(data=res, index=range(0, 24))


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
        # change to take into account only text messages
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
    
    def get_most_common_messages(self): # keep or change (?)
        return self.stats["Content"].value_counts()
    
    # 
    # TEXT REGULARIZATION AND NLP METHODS
    #

    def __createTextSubDataFrame(self):
        if self.stats is not None:
            self.__textSubDdf = self.stats[self.stats["Type"] == "Text"]
    
    
    def get_most_common_words(self):
        """
        Returns a dictionary with the words that appear in the chat and their count

        Returns
        --------------------
            words: dict
                Dictionary with word frequency
        """
        if self.__textSubDdf == None:
            self.__createTextSubDataFrame()

        words = Counter(
            (" ".join(self.__textSubDdf["Content"])).split()
            ) # save this as attribute to use later ?
        # returns dictionary (change to another type for better manupulation?)
        return words
    
    def get_most_common_words_per_user(self, user):
        if self.__textSubDdf == None:
            self.__createTextSubDataFrame()
        
        user_messages = self.__textSubDdf[self.__textSubDdf["Author"] == user]

        user_words = Counter(
            (" ".join(user_messages["Content"])).split()
        )
        return user_words

    def get_count_of_word(self, word):
        """
        Returns the number of times the input word appaeared in the chat
        """
        if self.__textSubDdf == None:
            self.__createTextSubDataFrame()
        
        words = Counter(
            (" ".join(self.stats["Content"])).split()
            )
        
        if word not in words.keys():
            return None
        
        return words[word]
    
    def text_regularization(self):
        """
        Method to regularize the chat messages
        """
        # create the text sub-dataframe
        self.__createTextSubDataFrame()
        #
        # Evaluate wheter to move __createTextSubDataFrame and tokenization 
        # methods inside of this function and the just use this for all preprocessing
        #
        # steps to implement:
        # - remove punctuation (non alpha-numeric characters)
        # - turn all words to lowercase 
        # - remove all stopwords
        self.__textSubDdf["tokenized"] = self.__textSubDdf["Content"].apply(
            lambda x: nltk.word_tokenize(x)   
        )

        # for stopwords topic modelling etc, do i have to detect what language the chat is in?
         