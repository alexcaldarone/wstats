import datetime
import dateutil.parser as datepars
import re

class Message:
    '''
    A class to contain info of a chat message

    Attributes
    --------------------
        self.date: str
            Contains the date on which the message was sent
        self.time: str
            Contains the time at which the message was sent
        self.author: str
            Contains the author of the message
        self.content: str
            Contains the content of the message (text or media)
        self.type: str
            Contains the type of the message (text, media or link)
        self.weekday: str
            Contains the weekday on which the day was sent
    '''

    # utility attibute used to determine wheter a message is a link or not
    __link_finder = re.compile("http(s://|://)")

    
    def __init__(self, chatline):
        '''constructor'''
        self.date = datepars.parse(chatline.split(',')[0],
                                   dayfirst=True) # this object is created only if the message is valid (tested before the message is created) the first number is interpreted as a day 
        self.__datelen = len(chatline.split(',')[0])
        self.time = chatline.split(',')[1][1:6] # change this to time object to handle better in analysis?
        self.__timelen = self.__datelen + 1+ len(self.time)
        self.author = self.def_author(chatline)
        self.__authlen = self.__timelen + 3 + len(self.author) + 2 # length of string until end of author name
        self.content = self.def_content(chatline)
        self.type = self.def_type(chatline)
        self.weekday = self.weekDayMessage()
    
    def to_list(self):
        attributes = [a for a in vars(self) if not a.startswith('_')]
        return [self.__getattribute__(a) for a in attributes]
    

    def is_valid_message(self, line): 
        '''
        Determines whether a line from the file is a valid message or the continuation of the previous message.
        A message is valid if the first characters are the date and the time of the message, otherwise it is the continuation
        of the previous message.

        Parameters
        --------------------
            line: str
                Line to be analyzed

        Returns
        --------------------
            True if the message is valid, False otherwise 
        '''
        try: 
            if datepars.parse(line.split(',')[0]):
                return True
        except Exception as e:
            return False
    
    def __str__(self):
        '''conversion to string'''
        return '{ Author:'+str(self.author)+' Date:'+str(self.date)+' Time:'+str(self.time)+' Type:'+str(self.type)+' \nContent:'+str(self.content)+' }'
    
    def def_author(self, chatline):
        '''
        Determines the author of the message

        Parameters
        --------------------
            chatline: str
                Line of the chat to be analyzed
        
        Returns
        --------------------
            author: str
                Author of the message
        '''
        authstr = chatline.split(',')[1][9:] # string where the author name is

        return authstr.split(':')[0]
    
    def def_content(self, chatline):
        '''
        Returns the content of the message

        Parameters
        --------------------
            chatline: str
                Line of the chat to be analyzed
        
        Returns
        --------------------
            Content of the message (str)
        '''
        return chatline[self.__authlen:]
    
    def def_type(self, chatline):
        '''
        Returns the type of the message

        Parameters
        --------------------
            chatline: str
                Line of the chat to be analyzed
        
        Returns
        --------------------
            messType: str
                Type of the message
        '''
        m = self.__link_finder.search(chatline[self.__authlen:])
        if m:
            messType = "Link"
        elif '<Media omitted>' in chatline[self.__authlen:]:
            messType = 'Media'
        else:
            messType = 'Text'
        return messType
    
    def weekDayMessage(self):
        '''
        Returns the day of the week on which the message was sent
        
        Returns
        --------------------
            Day of the week on which message was sent (str)
        '''
        weekNum = {0: 'Monday', 1:'Tuesday', 2:'Wednesday', 3:'Thursday', 4:'Friday', 5:'Saturday', 6:'Sunday'}
        weekday = self.date.weekday()
        return weekNum[weekday]