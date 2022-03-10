from io import StringIO
import streamlit as st
import datetime
import matplotlib.pyplot as plt

st.title("WhatsApp Stats")
st.markdown(''' #### _Discover the **secrets** behind your chats!_

With this simple app you will be able to analyze:
- :iphone: The total number of messages sent by each participant
- :date: How many messages were sent in each conversation
- :calendar: How many messages were sent on each conversation
- :watch: What time of day you chat the most
- :file_folder: How many of your messages are media 
- :speech_balloon: Who is the conversation starter?
- :memo: Who writes the longest messages on average?
-----
#### How does it work?
    - Open the chat you want to analyze in WhatsApp from your smartphone.
    - Click on the 3 dots, select More > Export chat
    - Choose to export without media
    - Import the text file in the app!
''')
chatfile = st.file_uploader("Upload your chat file.", type='txt')

# Functions to analyze chat
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
    stringio = StringIO(chatfile.getvalue().decode("utf-8"))
    chat_content = stringio.read().splitlines() # creates a list that contains the lines of the chat as strings
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
    try:
        if int(message.date[9]):
            if message.author in countdic.keys():
                countdic[message.author] += 1
            else:
                countdic[message.author] = 1
    except:
        pass
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
            try:
                avelength[i] = worddict[i]/mexnum[i]
            except KeyError:
                continue
    return avelength


if not chatfile:
    st.warning('No chat file uploaded')
    st.stop()
else:
    ## Chat analysis starts here
    chatlist = readFile(chatfile) 
    chat = checkList(chatlist)
    with st.spinner('Analyzing chat... This may take a few seconds.'):
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
        avelen = mexAveLength(numMessaggi, userWords)
        
        fig1, ax1 = plt.subplots()
        ax1.pie(list(numMessaggi.values()), labels=list(numMessaggi.keys()), autopct='%1.2f%%')
        ax1.axis('equal')

        fig2, ax2 = plt.subplots()
        ax2.bar(list(mexPerDay.keys()), list(mexPerDay.values()))
        ax2.set(xticklabels=[])
        ax2.set_ylabel('N° of messages')

        fig3, ax3 = plt.subplots()
        ax3.barh(list(mexWeekDay.keys())[::-1], list(mexWeekDay.values())[::-1])
        ax3.set_title('Weekly chatting patterns')

        fig4, ax4 = plt.subplots()
        ax4.bar(timeMex.keys(), timeMex.values())
        ax4.set_title('Houly chatting patterns')
        ax2.set_ylabel('N° of messages')

        fig5, ax5 = plt.subplots()
        ax5.pie(list(mexTypes.values()), labels=list(mexTypes.keys()), autopct='%1.2f%%')
        ax5.axis('equal')

        fig6, ax6 = plt.subplots()
        ax6.pie(list(beginMess.values()), labels=list(beginMess.keys()), autopct='%1.2f%%')
        ax6.axis('equal')

        fig7, ax7 = plt.subplots()
        ax7.barh(list(avelen.keys()), list(avelen.values()), align='center')
        ax7.set_yticks(list(avelen.keys()))
        ax7.invert_yaxis()  # labels read top-to-bottom
        ax7.set_xlabel('Average message length')
        ax7.set_title('Average participant message length')
    st.success('Done')
    

    st.header("Number of messages")
    col1, col2 = st.columns(2)
    with col1:
        st.metric('Total messages (includes update messages)', sum(numMessaggi.values()))
        for i in numMessaggi:
            if i != None and i != 'None':
                st.write(i+':', numMessaggi[i])
    with col2:
        st.pyplot(fig1)
    
    st.header("Messages sent per conversation")
    st.pyplot(fig2)
    
    st.header("Messages sent each weekday")
    col3, col4 = st.columns([1, 2])
    with col3:
        for i in mexWeekDay:
            st.write(i+':', mexWeekDay[i])
    with col4:
        st.pyplot(fig3)
    
    st.header('Hourly chatting patterns')
    st.pyplot(fig4)

    st.header("Type of message")
    col5, col6 = st.columns(2)
    with col5:
        st.write('Media includes photos, documents, audios.')
        for i in mexTypes:
            st.write(i+':', mexTypes[i])
    with col6:
        st.pyplot(fig5)
    
    st.header("Who were the conversations started by?")
    col7, col8= st.columns(2)
    with col7:
        st.metric('Total number of \nconversations', sum(beginMess.values()))
        for i in beginMess:
            if i != None:
                st.write(i, 'started', beginMess[i], 'conversations.')
    with col8:
        st.pyplot(fig6)
    
    st.header('Average message length')
    col9, col10 = st.columns(2)
    with col9:
        for i in avelen:
            if i != None:
                st.write(i+"'s average message length is:", round(avelen[i], 2))
    with col10:
        st.pyplot(fig7)
    
    st.markdown('''
    Created by [Alex Caldarone](https://alexcaldarone.github.io/)''')