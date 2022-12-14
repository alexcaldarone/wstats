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

    # st.write(analysis.get_messages_by_weekday())
    # st.write(analysis.stats)
    # st.write(analysis.get_messages_by_type())
    # st.write(analysis.get_messages_per_day_per_user())
    # st.write(analysis.get_messages_per_day())
    # st.write(analysis.get_chat_participants())
    # st.write(analysis.get_messages_by_hour())
    # st.write(analysis.average_message_length_by_user())
    # st.write(analysis.stats)
    # st.write(analysis.chats_started_by_user())
    # st.write(analysis.get_most_common_words())
    # st.write(analysis.stats)
    # st.write(analysis.get_most_common_words_per_user("User2"))
    # st.write(analysis.get_count_of_word("with"))
    # analysis.text_regularization()
    st.write(analysis.stats)

    """
    # Charts
    fig1, ax1 = plt.subplots()
    ax1.pie(list(analysis["Number"].values()), labels=list(analysis["Number"].keys()), autopct='%1.2f%%')
    ax1.axis('equal')

    fig2, ax2 = plt.subplots()
    ax2.bar(list(analysis["Days"].keys()), list(analysis["Days"].values()))
    ax2.set(xticklabels=[])
    ax2.set_ylabel('N° of messages')

    fig3, ax3 = plt.subplots()
    ax3.barh(list(analysis["Weekday"].keys()), list(analysis["Weekday"].values()))
    ax3.set_title('Weekly chatting patterns')

    fig4, ax4 = plt.subplots()
    ax4.bar(sorted(analysis["Time"].keys()), analysis["Time"].values()) # ricontrolla
    ax4.set_title('Houly chatting patterns')
    ax2.set_ylabel('N° of messages')

    fig5, ax5 = plt.subplots()
    ax5.pie(list(analysis["Type"].values()), labels=list(analysis["Type"].keys()), autopct='%1.2f%%')
    ax5.axis('equal')

    fig6, ax6 = plt.subplots()
    ax6.pie(list(analysis["Started"].values()), labels=list(analysis["Started"].keys()), autopct='%1.2f%%')
    ax6.axis('equal')

    fig7, ax7 = plt.subplots()
    ax7.barh(list(analysis["AveLength"].keys()), list(analysis["AveLength"].values()), align='center')
    ax7.set_yticks(list(analysis["AveLength"].keys()))
    ax7.invert_yaxis()  # labels read top-to-bottom
    ax7.set_xlabel('Average message length')
    ax7.set_title('Average participant message length')
    st.success('Done')

    st.header("Number of messages")
    col1, col2 = st.columns(2)
    with col1:
        st.metric('Total messages (includes update messages)', sum(analysis["Number"].values()))
        for i in analysis["Number"]:
            if i != None and i != 'None':
                st.write(i+':', analysis["Number"][i])
    with col2:
        st.pyplot(fig1)
    
    st.header("Messages sent per conversation")
    st.pyplot(fig2)
    
    st.header("Messages sent each weekday")
    col3, col4 = st.columns([1, 2])
    with col3:
        for i in analysis["Weekday"]:
            st.write(i+':', analysis["Weekday"][i])
    with col4:
        st.pyplot(fig3)
    
    st.header('Hourly chatting patterns')
    st.pyplot(fig4)

    st.header("Type of message")
    col5, col6 = st.columns(2)
    with col5:
        st.write('Media includes photos, documents, audios.')
        for i in analysis["Type"]:
            st.write(i+':', analysis["Type"][i])
    with col6:
        st.pyplot(fig5)
    
    st.header("Who were the conversations started by?")
    col7, col8= st.columns(2)
    with col7:
        st.metric('Total number of \nconversations', sum(analysis["Started"].values()))
        for i in analysis["Started"]:
            if i != None:
                st.write(i, 'started', analysis["Started"][i], 'conversations.')
    with col8:
        st.pyplot(fig6)
    
    st.header('Average message length')
    col9, col10 = st.columns(2)
    with col9:
        for i in analysis["AveLength"]:
            if i != None:
                st.write(i+"'s average message length is:", round(analysis["AveLength"][i], 2))
    with col10:
        st.pyplot(fig7)
    
    st.markdown("---")

    st.download_button(
        label="Download chat data as JSON",
        data=json.dumps(analysis.STATS, cls=SetEncoder),
        file_name="chat_stats.json",
        mime="text"
    )

    st.markdown("---")
    st.markdown('''
    Created by [Alex Caldarone](https://alexcaldarone.github.io/)''')"""
