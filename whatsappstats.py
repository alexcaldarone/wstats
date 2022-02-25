'''
Whatsapp chat analyzer
'''
from sys import argv
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
        Message.date = chatline[6:10]+'/'+chatline[3:5]+'/'+chatline[0:2]
        Message.time = chatline[12:17]
        Message.author = Message_author(chatline)
        Message.content = Message_content(chatline)
        Message.type = Message_type(chatline)
    
    ## converisone a stringa
    def __str__(self):
        return '{ Author:'+str(self.author)+' Date:'+str(self.date)+' Time:'+str(self.time)+' Type:'+str(self.type)+' \nContent:'+str(self.content)+' }'


## Determina il tipo di messaggio
# @param chatline (str) messaggio
# @return messType (str) tipo di messaggio
def Message_type(chatline):
    if '<Media omitted>' in chatline:
        messType = 'Media'
    elif 'https://' in chatline:
        messType = 'Link'
    else:
        messType = 'Text'
    return messType

## Restituisce il contenuto del messagio
# @param chatline (str) messaggio
# @return (str) contenuto del messaggio
def Message_content(chatline):
    if Message.author == None:
        return chatline[21:]
    else:
        return chatline[21+len(Message.author):]

## Determina l'autore di un messaggio
# @param chatline (str) messaggio
# @return author (str) autore del messaggio
def Message_author(chatline):
    author = ''
    if ':' not in chatline:
        author = 'None'
        return author
    for i in range(20, len(chatline)):
        if chatline[i] == ':':
            return author
        else:
            author += chatline[i]


## Apre il file di una chat e restituisce una lista di stringhe dei messaggi
# @param chatfile (file) file di testo di una chat
# @return chat_content (str) stinga con i contenuti della chat
def readFile(chatfile):
    chat = open(chatfile, 'r', encoding='utf-8')
    chat_content = chat.read().splitlines() # creates a list that contains the lines of the chat as strings
    chat.close()
    return chat_content

## Controlla che i primi caratteri di una stringa siano la data. Se non lo sono aggiunge le stringa a quella precedente
## e poi la rimuove.
# @param chatlist (list) lista di stringhe
# @return chatlist (lsita) lista di stringhe aggiornata
def checkList(chatlist):
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] # list used to check if first characters are date
    removel = [] # list of indexes to remove
    for i in range(1, len(chatlist)):
        for j in chatlist[i][0:2]+chatlist[i][3:5]+chatlist[i][6:10]:
            if j not in numbers:
                if i not in removel:
                    removel.append(i)
                    chatlist[i-1] += chatlist[i]
                break
    for i in range(0, len(removel)):
        chatlist = chatlist[:removel[i]-i]+chatlist[removel[i]-i+1:]
    return chatlist

## Conta il numero di messaggi inviati da ogni partecipante
# @param countdic (dict) dizionario dove riportare i messaggi inviati da ogni partecipante
# @param message (Message) messaggio da contare
# @return countdic (dict) dizionario aggiornato
def countMessage(countdic, message):
    if message.author in countdic.keys():
        countdic[message.author] += 1
    else:
        countdic[message.author] = 1
    return countdic

## Conta il numero di messaggi inviati ogni giorno
# @param daydict (dict) dizionario dove riportare il numero di messaggi giornalieri
# @param message (Message) messaggio
# @return daydict (dict) dizionario aggiornato
def dayMessage(daydict, message):
    if message.date in daydict.keys():
        daydict[message.date] += 1
    else:
        daydict[message.date] = 1
    return daydict

## Conta il numero di messaggi inviati nei vari giorni della settimana
# @param weekdict (dict) dizionario dove riportare i messaggi inviati nei vari giorni della settimana
# @param message (Message) messaggio da analizzare
# @return weekdict (dict) dizionario aggiornato
def weekDayMessage(weekdict, message):
    weekNum = {0: 'Monday', 1:'Tuesday', 2:'Wednesday', 3:'Thursday', 4:'Friday', 5:'Saturday', 6:'Sunday'}
    dayNum = datetime.date(int(message.date[0:4]), int(message.date[5:7]), int(message.date[8:10])).weekday()
    weekdict[weekNum[dayNum]] += 1
    return weekdict

## Conta quanti messaggi appartengono an ogni categoria
# @param typedict (dict) dizionario dove riportare il numero di messaggi dei vari tipi
# @param message (Message) messaggio da analizzare
# @return typedict (dict) dizionario aggiornato
def typeOfMessage(typedict, message):
    if message.type in typedict.keys():
        typedict[message.type] += 1
    else:
        typedict[message.type] = 1
    return typedict

## Conta i messagi inviati nel corso delle 24 ore giornaliere
# @param timedict (dict) dizionario con orari
# @param message (Message) messaggio da analizzare
# @return timedict (dict) dizionario aggiornato
def timeMessage(timedict, message):
    timedict[message.time[0:2]] += 1
    return timedict

## Determina il numero di conversazioni iniziate da ogni partecipante
# @param autdict (dict) dizionario dove riportare il numero di conversazioni inziate dai partecipanti
# @param messagelist (lista di Message) lista di messaggi
# @param lastdate (str) data del messaggio precedente a quello corrente
# @return autdict (dict) dizionario aggiornato
def chatBegins(autdict, messagelist, lastdate):
    if len(messagelist) == 1:
        autdict[messagelist[0].author] = 1
    else:
        if messagelist[-1].date != lastdate:
            if messagelist[-1].author in autdict:
                autdict[messagelist[-1].author] += 1
            else:
                autdict[messagelist[-1].author] = 1
    return autdict

## Conta il numero di parole in un messaggio
# @param message (Message) messaggio
# @return count (int) numero di parole nel messaggio
def wordcounter(message):
    count = 0
    if message.type == 'Text':
        for i in range(len(message.content)):
            if message.content[i] == ' ':
                count += 1
    return count

## Conta il numero di parole inviate da ogni partecipante
# @param worddict (dict) dizionario dove riportare le parole di ogni partecipante
# @param message (Message) messaggio da analizzare
# @return worddict (dict) dizionario aggiornato
def wordPerUser(worddict, message):
    if message.author in worddict:
        worddict[message.author] += wordcounter(message)
    else:
        worddict[message.author] = wordcounter(message)
    return worddict

## Restituisce la lunghezza media dei messaggi di ogni utente
# @param mexnum (dict) dizionario con numero di messaggi inviati da ogni partecipante
# @param worddict (dict) dizionario con numero di parole inviate da ogni partecipante
# @return avelength (dict) dizionario con lunghezza media dei messaggi di ogni partecipante
def mexAveLength(mexnum, worddict):
    avelength = dict()
    for i in mexnum:
        if i == None:
            continue
        else:
            avelength[i] = worddict[i]/mexnum[i]
    return avelength

# Main
def main():
    chatfile = readFile(argv[1]) # change readChat function
    chat = checkList(chatfile)
    
    MessageList = []
    numMessaggi = dict()
    mexPerDay = dict()
    mexWeekDay = {'Monday':0, 'Tuesday':0, 'Wednesday':0, 'Thursday':0, 'Friday':0, 'Saturday':0, 'Sunday':0}
    mexTypes = dict()
    beginMess = dict()
    lastdate = ''
    timeMex = {'00': 0, '01': 0, '02':0, '03':0, '04':0, '05':0, '06':0, '07':0, '08':0, '09':0, '10':0, '11':0,
    '12':0, '13':0, '14':0, '15':0, '16':0, '17':0, '18':0, '19':0, '20':0, '21':0, '22':0, '23':0}
    userWords = dict()
    for i in range(1, len(chat)):
        MessageList.append(Message(chat[i]))
        numMessaggi = countMessage(numMessaggi, MessageList[i-1])
        mexPerDay = dayMessage(mexPerDay, MessageList[i-1])
        try:
            mexWeekDay = weekDayMessage(mexWeekDay, MessageList[i-1])
        except ValueError:
            continue
        mexTypes = typeOfMessage(mexTypes, MessageList[i-1])
        timeMex = timeMessage(timeMex, MessageList[i-1])
        beginMess = chatBegins(beginMess, MessageList, lastdate)
        lastdate = MessageList[i-1].date
        userWords = wordPerUser(userWords, MessageList[i-1])
    
    print('''
    --------------------------
    | WHATSAPP CHAT ANALYSER |
    --------------------------

    -- NUMBER OF MESSAGES --
    ''')
    for i in numMessaggi:
        print('Autore:', i, 'Numero messaggi:', numMessaggi[i])
    print('Numero totale messaggi:', sum(numMessaggi.values()))
    print('''
    -- DAYS OF MESSAGES --
    ''')
    for i in mexPerDay:
        print('Data:', i, 'Messagi:', mexPerDay[i])
    print('''
    -- WEEKDAY OF MESSAGES --
    ''')
    for i in mexWeekDay:
        print('Weekday:', i, 'Messages:', mexWeekDay[i])
    print('''
    -- TYPE OF MESSAGES --
    ''')
    for i in mexTypes:
        print('Type', i, 'N° of messages:', mexTypes[i])
    print('''
    -- MESSAGES TIME PATTERNS --
    ''')
    for i in timeMex:
        print('Hour:', i, 'N° of messages:', timeMex[i])
    print('''
    -- WHO WERE THE CHATS STARTED BY? --
    ''')
    for i in beginMess:
        print(i, 'started', beginMess[i], 'chats.')
    print('''
    -- TOTAL WORDS SENT --
    ''')
    for i in userWords:
        print(i, 'sent a total of', userWords[i], 'words.')
    print('''
    -- AVERAGE MESSAGE LENGTH --
    ''')
    avelen = mexAveLength(numMessaggi, userWords)
    for i in avelen:
        print(str(i)+"'s average message length is:", avelen[i])


# Avvio
main()