import datetime
## Classe Message
# @var author (str) autore del messaggio
# @var date (str) data di invio del messaggio
# @var time (str) orario di invio del messaggio
# @var content (str) contenuto del messaggio
# @var type (str) tipo di messaggio
class Message:
    ## costruttore
    # @param chatline (str) stringa del messaggio
    # @return (Message) tipo costruito
    def __init__(self, chatline):
        self.date = chatline[6:10]+'/'+chatline[3:5]+'/'+chatline[0:2]
        self.time = chatline[12:17]
        self.author = self.def_author(chatline)
        self.content = self.def_content(chatline)
        self.type = self.def_type(chatline)
        self.weekday = self.weekDayMessage()
    
    def is_valid_message(self, line): # sposta all'interno del costruttore di Message 
        '''
        Determines whether a line from the file is a valid message or the continuation of the previous message.
        A message is valid if the first characters are the date and the time of the message, otherwise it is the continuation
        of the previous message
        '''
        try: 
            if datetime.date(int(line[6:10]), int(line[3:5]), int(line[0:2])) and datetime.time(int(line[12:14]), int(line[15:17])):
                return True
        except:
            return False
    
    ## converisone a stringa
    def __str__(self):
        return '{ Author:'+str(self.author)+' Date:'+str(self.date)+' Time:'+str(self.time)+' Type:'+str(self.type)+' \nContent:'+str(self.content)+' }'
    
    ## Determina l'autore di un messaggio
    # @param chatline (str) messaggio
    # @return author (str) autore del messaggio
    def def_author(self, chatline):
        author = ''
        if ':' not in chatline:
            author = 'None'
            return author
        for i in range(20, len(chatline)):
            if chatline[i] == ':':
                return author
            else:
                author += chatline[i]
    
    ## Restituisce il contenuto del messagio
    # @param chatline (str) messaggio
    # @return (str) contenuto del messaggio
    def def_content(self, chatline):
        if self.author == None:
            return chatline[21:]
        else:
            return chatline[21+len(self.author):]
    
    ## Determina il tipo di messaggio
    # @param chatline (str) messaggio
    # @return messType (str) tipo di messaggio
    def def_type(self, chatline):
        if '<Media omitted>' in chatline:
            messType = 'Media'
        elif 'https://' in chatline:
            messType = 'Link'
        else:
            messType = 'Text'
        return messType
    
    def weekDayMessage(self):
        weekNum = {0: 'Monday', 1:'Tuesday', 2:'Wednesday', 3:'Thursday', 4:'Friday', 5:'Saturday', 6:'Sunday'}
        weekday = datetime.date(int(self.date[0:4]), int(self.date[5:7]), int(self.date[8:10])).weekday()
        return weekNum[weekday]