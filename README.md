[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://chatstats.streamlit.app/)
[![Tests](https://github.com/alexcaldarone/wstats/actions/workflows/tests.yml/badge.svg)](https://github.com/alexcaldarone/wstats/actions/workflows/tests.yml)

# WhatsApp Stats
WhatsApp Stats is a streamlit app that allows you to parse and analyze whatsapp chats! 

With this simple app you will be able to analyze:
- :iphone: The total number of messages sent by each participant
- :date: How many messages were sent in each conversation
- :calendar: How many messages were sent on each conversation
- :watch: What time of day you chat the most
- :file_folder: How many of your messages are media 
- :speech_balloon: Who is the conversation starter?
- :memo: Who writes the longest messages on average?

## Table of Contents

- [Usage](#usage)
- [To Do](#todo)

## Usage
You can use this app directly on Streamlit through this [link](https://chatstats.streamlit.app/)

Otherwise, to run this app locally you can run the following commands

```shell
git clone https://github.com/alexcaldarone/wstats.git
cd wstats
pip install -r requirements.txt
python setup.py install
streamlit run main_page.py
```


## To Do:
- Add linter
