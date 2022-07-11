import streamlit as st
import matplotlib.pyplot as plt
from scripts.message import Message
from scripts.analysis import Analysis
from io import StringIO

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
    analysis = Analysis()
    stringio = StringIO(chatfile.getvalue().decode("utf-8"))
    for line in stringio:
        chatline = line.strip()
        if analysis.is_valid_message(line):
            message = Message(line)
            analysis.update_stats(message)
        else:
            pass