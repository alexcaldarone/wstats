from message import Message
from io import StringIO
import datetime

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