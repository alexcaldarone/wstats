import streamlit as st
import matplotlib.pyplot as plt
from message import Message
from analysis import *

st.title("WhatsApp Stats")
st.markdown(''' #### _Discover the **secrets** behind your chats!_

With this simple app you will be able to analyze:
- :iphone: The total number of messages sent by each participant
- :date: How many messages were sent in each conversation
- :calendar: How many messages were sent on each day
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