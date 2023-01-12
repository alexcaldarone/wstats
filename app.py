import streamlit as st
import matplotlib.pyplot as plt
import json
from io import StringIO
from scripts.message import Message
from scripts.analysis import Analysis
from scripts.json_set_encoder import SetEncoder
import time

st.set_page_config(page_title="WhatsApp Stats")
st.title("WhatsApp Stats")
st.markdown(''' #### _Discover the **secrets** behind your chats!_

With this simple app you will be able to analyze:
- :iphone: The total number of messages sent by each participant
- :incoming_envelope: How many messages were sent in each conversation
- :calendar: How many messages were sent on each weekday
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
    analysis = Analysis()
    stringio = StringIO(chatfile.getvalue().decode("utf-8"))
    last_message_analyzed = None
    for i, line in enumerate(stringio):
        if i == 0:
            continue  # skip first chat line
        #chatline = line.strip()
        if Message.is_valid_message(Message, line):  # check if the line is valid message
            message = Message(line.strip()) 
            last_message_analyzed = analysis.update_list(message)
        else:  # if it isn't a valid message then it's the continuation of the previous message
            if last_message_analyzed:
                analysis.update_last_message(line)
    
    analysis.generate_dataframe()
    analysis.text_regularization()
    # Charts

    # Number of messages sent by each user
    messages_by_user = analysis.get_messages_per_user()
    fig1, ax1 = plt.subplots()
    ax1.pie(messages_by_user, labels=messages_by_user.index, autopct='%1.2f%%')
    ax1.axis('equal')
    
    # Number of messages per conversation
    number_of_messager_per_conversation = analysis.get_messages_per_day()
    fig2, ax2 = plt.subplots()
    ax2.plot(number_of_messager_per_conversation.index, number_of_messager_per_conversation)
    #ax2.set(xticklabels=[])
    ax2.set_ylabel('N° of messages')

    # number of messages per weekday
    number_of_messager_per_weekday = analysis.get_messages_by_weekday()
    fig3, ax3 = plt.subplots()
    ax3.barh(number_of_messager_per_weekday.index[::-1], number_of_messager_per_weekday[::-1])
    ax3.set_title('Weekly chatting patterns')

    # number of messages per hour
    number_of_messages_per_hour = analysis.get_messages_by_hour()
    fig4, ax4 = plt.subplots()
    ax4.bar(number_of_messages_per_hour.index, number_of_messages_per_hour) 
    ax4.set_title('Houly chatting patterns')
    ax2.set_ylabel('N° of messages')

    # Number of messages for each message type (text, media, link)
    number_of_messages_per_type = analysis.get_messages_by_type()
    fig5, ax5 = plt.subplots()
    ax5.pie(number_of_messages_per_type, labels=number_of_messages_per_type.index, autopct='%1.2f%%')
    ax5.axis('equal')

    # Number of conversations started by each user
    conversation_started_by_users = analysis.chats_started_by_user()
    fig6, ax6 = plt.subplots()
    ax6.pie(conversation_started_by_users, labels=conversation_started_by_users.index, autopct='%1.2f%%')
    ax6.axis('equal')

    # Average message length for each message
    average_message_length = analysis.average_message_length_by_user()
    fig7, ax7 = plt.subplots()
    ax7.barh(average_message_length.index, average_message_length, align='center')
    ax7.set_yticks(average_message_length.index)
    ax7.invert_yaxis()  # labels read top-to-bottom
    ax7.set_xlabel('Average message length')
    ax7.set_title('Average participant message length')
    st.success('Done')

    # Display charts

    st.header("Number of messages")
    col1, col2 = st.columns(2)
    with col1:
        st.metric('Total messages (includes update messages)', sum(messages_by_user))
        for i in messages_by_user.index:
            if i != None and i != 'None':
                st.write(i+':', messages_by_user[i])
    with col2:
        st.pyplot(fig1)
    

    st.header("Messages sent per conversation")
    st.bar_chart(data = number_of_messager_per_conversation)

    
    st.header("Messages sent each weekday")
    col3, col4 = st.columns([1, 2])
    with col3:
        for i in number_of_messager_per_weekday.index:
            st.write(i+':', number_of_messager_per_weekday[i])
    with col4:
        st.pyplot(fig3)
    
    
    st.header('Hourly chatting patterns')
    st.pyplot(fig4)


    st.header("Type of message")
    col5, col6 = st.columns(2)
    with col5:
        st.write('Media includes photos, documents, audios.')
        for i in number_of_messages_per_type.index:
            st.write(i+':', number_of_messages_per_type[i])
    with col6:
        st.pyplot(fig5)
    
    
    st.header("Who were the conversations started by?")
    col7, col8= st.columns(2)
    with col7:
        st.metric('Total number of \nconversations', sum(conversation_started_by_users))
        for i in conversation_started_by_users.index:
            if i != None:
                st.write(i, 'started', conversation_started_by_users[i], 'conversations.')
    with col8:
        st.pyplot(fig6)
    
    
    st.header('Average message length')
    col9, col10 = st.columns(2)
    with col9:
        for i in average_message_length.index:
            if i != None:
                st.write(i+"'s average message length is:", round(average_message_length[i], 2))
    with col10:
        st.pyplot(fig7)
    
    st.header("How often was a certain word used?")
    input_word = st.text_input("Search for word")
    if input_word != None:
        word_frequency = analysis.get_count_of_word_per_conversation(input_word.lower())
        fig8, ax8 = plt.subplots()
        ax8.scatter(word_frequency.index, word_frequency)
        ax8.set_ylim(bottom=0)
        st.pyplot(fig8)
    
    # add distribution of words per user (?)

    # add count of a single word

    # add most common words for a certain user
    st.header("What is a user's most common word?")
    st.write("Returns the selected user's 5 most common words.")
    col11, col12 = st.columns(2)
    with col11:
        selected_user = st.radio(
            label="Select a user",
            options=analysis.get_chat_participants()
        )
    most_common_words_per_user = analysis.get_most_common_words_per_user(selected_user)
    with col12:
        for word in most_common_words_per_user:
            st.write(word)

    st.markdown("---")
    st.markdown('''
    Created by [Alex Caldarone](https://alexcaldarone.github.io/)''')
