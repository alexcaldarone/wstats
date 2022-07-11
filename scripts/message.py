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
        Message.date = chatline[6:10]+'/'+chatline[3:5]+'/'+chatline[0:2]
        Message.time = chatline[12:17]
        Message.author = Message.def_author(self, chatline)
        Message.content = Message.def_content(self, chatline)
        Message.type = Message.def_type(self, chatline)
    
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
        if Message.author == None:
            return chatline[21:]
        else:
            return chatline[21+len(Message.author):]
    
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