import streamlit as st
from scripts.classifier import NaiveBayesClassifier
from io import BytesIO

st.set_page_config(page_title="WhatsApp Stats")
st.sidebar.markdown("# Message Classifier")
st.sidebar.markdown("Who is most likely to have written a messgae?")
st.sidebar.markdown("Find out!")

st.title("Message Classifier")
st.markdown("""This page uses a **Multinomial Naive Bayes Classifier** to find out 
           who is the most likely author of a given message""")


parquet_file = st.file_uploader(label="Upload chat parquet file", type="parquet")

if not parquet_file:
    st.warning("Please upload the parquet file to train the model.")
    st.stop()
else:
    nb = NaiveBayesClassifier()
    nb.get_raw_data(parquet_file)
    nb.create_corpus()
    authors = nb.raw_data["Author"].unique()
    estimator, vectorizer = nb.training_pipeline()
    
    input = st.text_input(label="Write the message here!") # isert string to classify

    if not input:
        st.warning("Please write a message to see the classifier's result.")
        st.stop()
    else:
        most_likely_class, most_likely_prob = nb.classify_text(input, estimator, vectorizer, labels=authors)

        st.write(f"""The classifier detected that the most likely author of the input
        message was {most_likely_class} with a probability of {most_likely_prob}""")

        # add possible observations/disclaimers ?