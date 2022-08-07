import datetime

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
    def __init__(self, chatline):
        '''constructor'''
        self.date = datetime.datetime.strptime(chatline[:17], '%d/%m/%Y, %H:%M')
        self.time = chatline[12:17]
        self.author = self.def_author(chatline)
        self.content = self.def_content(chatline)
        self.type = self.def_type(chatline)
        self.weekday = self.weekDayMessage()
    
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
            if datetime.datetime.strptime(line[:17], '%d/%m/%Y, %H:%M'):
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
        author = ''
        if ':' not in chatline:
            author = 'None'
            return author

        return chatline[18:].split(':')[0]
    
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
        if self.author == None:
            return chatline[21:]
        else:
            return chatline[21+len(self.author):]
    
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
        if '<Media omitted>' in chatline:
            messType = 'Media'
        elif 'https://' in chatline:
            messType = 'Link'
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
