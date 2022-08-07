from scripts.message import Message

class Analysis:
    '''
    A class to contain the statistics of a whatsapp chat

    Attributes
    --------------------
        self.STATS: dict
            Dictionary containing the statistics of the chat
        self.last_date: str
            Saves the date of the last message analyzed (used to determine who started a conversation)
    '''
    STATS = {
        # Keeps track of the participants of the chat
        "Participants": set(),
        # Keeps track of the days in which the conversations happen
        "Weekday": {
            "Monday": 0,
            "Tuesday": 0,
            "Wednesday": 0,
            "Thursday": 0,
            "Friday": 0,
            "Saturday": 0,
            "Sunday": 0
        },

        # Keeps track of the time at which the conversations happen
        "Time": {

        },

        # Keeps track of the number of conversations started by each participant
        "Started": {

        },

        # keeps track of the average message length for each user
        "AveLength": {

        },

        # keeps track of the types of each message
        "Type":{

        },

        # Keeps track of how many messages were sent on each day
        "Days": {

        },

        # Keeps track of the number of messages sent by each participant
        "Number": {

        },
        # keeps track of the number of words sent by each participant
        "NumberWords": {

        }
    }

    def __init__(self):
        '''Constructor'''
        # clearing dictionaries 
        self["Participants"].clear()
        self["Time"].clear()
        self["Started"].clear()
        self["AveLength"].clear()
        self["Days"].clear()
        self["Number"].clear()
        self["NumberWords"].clear()
        self["Type"].clear() # resets all the values of the type dictionay to zero
        self.last_date = None # attribute used to determine who started a conversation

    def update_stats(self, message: Message): # make all the dictionary checks the same
        '''
        Updates the STATS dictionary with the statistics from a message passed as argument

        Parameters
        --------------------
            message: Message 
                object containing the message to analyze
        '''
        # days
        message_date = str(message.date)
        if message_date not in self["Days"].keys():
            self["Days"][message_date] = 1
        else:
            self["Days"][message_date] += 1
            self.last_date = message.date  # save last date analyzd for comparison needed to see who started the chat
        # weekday
        self["Weekday"][message.weekday] += 1
        # participant
        if message.author not in self["Participants"]:
            self["Participants"].add(message.author)
        # type
        if message.type not in self["Type"]:
            self["Type"][message.type] = 1
        else:
            self["Type"][message.type] += 1
        # number of messages sent
        if message.author not in self["Number"].keys():
            self["Number"][message.author] = 1
        else:
            self["Number"][message.author] += 1
        # who began the chat
        self.chatBegins(message)
        # time
        if message.time[0:2] not in self["Time"].keys():
            self["Time"][message.time[0:2]] = 1
        else:
            self["Time"][message.time[0:2]] += 1
        # word counter
        if message.author in self["NumberWords"].keys():
            self["NumberWords"][message.author] += len(message.content.split(' '))
        else:
            self["NumberWords"][message.author] = len(message.content.split(' '))
        print(self.STATS)
  
    def chatBegins(self, message: Message):
        '''
        Determines who started the chat

        Parameters
        --------------------
            message: Message 
                object containing the message to analyze
        '''
        if self.last_date != message.date: 
            if message.author in self["Started"].keys():
                self["Started"][message.author] += 1
            else:
                self["Started"][message.author] = 1
    
    def __getitem__(self, st):
        '''
        Returns the dictionary in STATS with name $st

        Parameters
        --------------------
            st: str
                Name of dictionary to be returned
        
        Returns
        --------------------
            self.STATS[st]: dict
        '''
        if st in self.STATS.keys():
            return self.STATS[st]
        else:
            raise IndexError("Category not present in the stats.")
    
    def calculate_avelength(self):
        '''
        Calculates the average length of the messages sent by each participant in the chat
        '''
        for p in self["Participants"]:
            if p != None:
                self["AveLength"][p] = self["NumberWords"][p] / self["Number"][p]


if __name__ == '__main__':
    a = Analysis()
    print(a["Weekday"])
