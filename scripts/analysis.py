from scripts.message import Message
import nltk
from nltk.corpus import stopwords
import pandas as pd
from collections import Counter
import emoji
import streamlit as st

# grabbing stpowords from nltk
english_stop_words = stopwords.words("english")
italian_stop_words = stopwords.words("italian")
stop_words = set(english_stop_words + italian_stop_words)

class Analysis:
    """
    Extra features to add:
        --- frequency of most used words by each user (nltk.freqDist)
        --- possibility to choose a word and see how many times it has been used (globally and for each user)
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
        
        df = pd.DataFrame(self.__tempList, 
            columns= ["Date", "Time", "Author", "Content", "Type", "Weekday"])
        
        # dropping rows where there is no messagecd 
        self.stats = df.loc[(df["Content"] != "") & (df["Content"] != " ")]
    
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
        # do with dictionary ?
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
        return True
    
    
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
        
        return words
    
    
    def get_most_common_words_per_user(self, user):
        """
        Returns the most common words used by each user
        
        Parameters
        --------------------
            user: str
                Chat participant
        Returns
        --------------------
            user_words: dict
                Dictionary with most common words that appear in the user's messages
        """
        if user not in self.get_chat_participants():
            raise Exception(f"{user} not in the chat participants!")
        
        if self.__textSubDdf is None:
            self.__createTextSubDataFrame()
        
        user_messages = self.__textSubDdf[self.__textSubDdf["Author"] == user]
        
        st = "" 
        for idx, row in user_messages.iterrows(): # can i do it with lists instead of strings
            st += " " + " ".join(user_messages["tokenized"][idx])
        
        words_string = Counter(st.split())
        top_frequencies = sorted(list(words_string.values()))[-5::] # get the frequencies of the 5 most used words
        most_common_words = [word for word in words_string.keys() if words_string[word] in top_frequencies]

        return most_common_words[:5] # return only top 5 words
    
    
    def get_count_of_word(self, word):
        """
        Returns the number of times the input word appaeared in the chat
        
        Parameters
        --------------------
            word: str
                The word whose frequency we want to track
        Returns
        --------------------
            words: int
                Word's frequency in the chat
        """
        if self.__textSubDdf == None:
            self.__createTextSubDataFrame()
        
        words = Counter(
            (" ".join(self.stats["Content"])).lower().split()
            ) # getting the number of times a certain word has been used in the chat
        
        if word.lower() not in words.keys(): # if the word has not been used return none
            return None
        
        return words[word.lower()] # otherwise return the number of times it appeared
    
    
    def get_count_of_word_per_conversation(self, word):
        """
        Returns the number of times a word appears in each conversation.

        Parameters
        --------------------
            word: str
                The word whose frequency we want to track over time
        Returns
        --------------------
            pd.Series
                Pandas Series with word count for each conversation 
        """
        # do it with regularized text
        if self.__textSubDdf is None:
            self.__createTextSubDataFrame()
        
        dates = pd.unique(self.__textSubDdf["Date"]) # getting the unique dates
        # merged_token_list = [] # list to 
        word_appearances = [0] * len(dates) # empty list to store the number of times a word apperared

        for i, date in enumerate(dates): # iterating over the dates
            conversation = self.__textSubDdf[self.__textSubDdf["Date"] == date] # getting the messages from a particular day

            word_count = Counter(
            (" ".join(conversation["Content"])).lower().split()
            ) # turning the content to a list and creating a counter

            if word in word_count.keys(): # if the word we are looking for has been used
                word_appearances[i] = word_count[word] # we update the list with the number of times it appeared
        
        return pd.Series(data=word_appearances, index=dates)

    
    def text_regularization(self):
        """
        Method to regularize the chat messages
        """
        # create the text sub-dataframe
        self.__createTextSubDataFrame()

        # converting emoji to text
        self.__textSubDdf["Content"] = self.__textSubDdf["Content"].apply(
            lambda x: emoji.demojize(x)
        )

        # turning all words to lowercase
        self.__textSubDdf["Content"] = self.__textSubDdf["Content"].apply(
            lambda x: x.lower()
        )

        # tokenizing the messages using nltk
        self.__textSubDdf["tokenized"] = self.__textSubDdf["Content"].apply(
            lambda x: nltk.word_tokenize(x)   
        )

        # removing the stopwords
        self.__textSubDdf["tokenized"] = self.__textSubDdf["tokenized"].apply(
            lambda x: [word for word in x if not word in stop_words]
        )

        # removing punctuation
        self.__textSubDdf["tokenized"] = self.__textSubDdf["tokenized"].apply(
            lambda x: [word for word in x if word not in "!£$%&/()=?'^[]}{+*#°@-_.:,;\|<>"]
        )

        return self.__textSubDdf
    
    @st.cache
    def export_to_classifier(self):
        """
        Export the tokenized messages and the author columns as a parquet file.
        """
        return self.__textSubDdf[["Author", "tokenized"]]