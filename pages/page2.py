import streamlit as st

from scripts.classifier import NaiveBayesClassifier
 

st.set_option('deprecation.showPyplotGlobalUse', False) # silence matplotlib deprecation warnings
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
    with st.spinner("Training model..."):
        nb = NaiveBayesClassifier()
        nb.get_raw_data(parquet_file)
        nb.create_corpus()
        authors = nb.raw_data["Author"].unique()
        estimator, vectorizer = nb.training_pipeline()
    st.success("Model trained!")

    st.write(f"The model's f1-score is: {round(nb.f1_score, 2)}")

    st.subheader("Confusion matrix")
    st.pyplot(nb.confusion_matrix)
    
    input = st.text_input(label="Write the message here!") # insert string to classify

    if not input:
        st.warning("Please write a message to see the classifier's result.")
        st.stop()
    else:
        most_likely_class, most_likely_prob = nb.classify_text(input, estimator, vectorizer, labels=authors)

        st.write(f"""The classifier detected that the most likely author of the input
        message was {most_likely_class} with a probability of {round(most_likely_prob, 2)}""")

        
        st.markdown("""
        **A few notes on the model's accuracy**
        
        1. The performance of the model is impacted by the amount of training data, so it tends to perform poorly on chats with few messages
        
        2. If the users in a chat share a very similar vocabulary the performance of the model will suffer
        
        3. The model seems to be biased towards the "most active user in the chat" (i.e. if there is one user who messages more than others the model will tend to classify the input messages as his, this is because of an imbalance of the labels in the training data) 
        """)