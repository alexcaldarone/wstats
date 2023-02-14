# imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn import model_selection
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.model_selection import train_test_split, cross_validate
from sklearn.naive_bayes import MultinomialNB

class NaiveBayesClassifier():
    """
    Class used to define the training pipeline used for the model and to make predictions.
    """

    def get_raw_data(self):
        """
        Reads a parquet file and initializes the raw_data attribute where the data is stored as a pandas dataframe
        """
        self.raw_data = pd.read_parquet("../classifier_raw_data.parquet",
                                        engine="pyarrow")
    
    def create_corpus(self):
        """
        Converts the elements in the tokenized column from lists to strings and creates a list containing the corpus
        used to train the model.

        Returns
        --------------------
            list
                The corpus used to train the model
        """
        corpus = []
        for index, row in self.raw_data.iterrows():
            st = " ".join(row["tokenized"])
            self.raw_data["tokenized"][index] = st
            corpus.append(st)
        return corpus # don't need corpus list ?
    
    def training_pipeline(self):
        """
        Method to contain the training pipeline for the model.
        Returns the best estimator found and the vectorizer used in the training process

        Returns
        --------------------
            CountVectorizer
                Vectorizer used in the training process to vectorize the corpus
            
            ...
                The best estimator found during the training process
        """
        Y = self.raw_data.pop("Author") # change to use imput corpus instead of attributes?
        
        train_data, test_data, train_label, test_label = train_test_split(self.raw_data["tokenized"],
                                                                          Y,
                                                                          train_size=0.8,
                                                                          random_state=2)
        
        vectorizer = CountVectorizer(ngram_range=(1,3)) 
        train_vects = vectorizer.fit_transform(train_data)
        test_vects = vectorizer.transform(test_data)

        params = {'alpha': [0.01, 0.1, 0.5, 1.0, 10.0,],}
        multinomial_grid_search = model_selection.GridSearchCV(MultinomialNB(), 
                                                               param_grid=params, 
                                                               scoring="f1_macro", 
                                                               n_jobs=-1, # use all processors 
                                                               cv=5,
                                                               verbose=5)
        multinomial_grid_search.fit(train_vects, train_label)
        print('Best parameter value(s): {}'.format(multinomial_grid_search.best_params_)) # print out the best parameters

        best_nb_classifier = multinomial_grid_search.best_estimator_ # grabbing the best estimator
        test_preds = best_nb_classifier.predict(test_vects) # make prediction on the test set using best estimator
        print('Validation F1 score with grid searchc: {}'.format(metrics.f1_score(test_preds, test_label, average='macro'))) # print out the f1 score

        # cv_score = cross_validate(best_nb_classifier, test_vects, test_label, cv=5)

        return best_nb_classifier, vectorizer


    def classify_text(self, text, classifier, vectorizer, labels=None):
        """
        Method to classify a given piece of text

        Parameters
        --------------------
            text: str
                Piece of text to classify
            classifier: ..
                Classifier used to classify the text
            vectorizer: CountVectorizer
                Vectorizer used to vectorize the piece of text to classify
            labels: list
                Labels to be predicted by the model
        
        Returns
        --------------------
            tuple
                Tuple containing the most likely class and the probability assigned to it.
        """
        vects = vectorizer.transform([text])
        probs = classifier.predict_proba(vects).flatten()
        max_prob_idx = np.argmax(probs)

        if labels: # if labels are given return the most likely label
            max_prob_class = labels[max_prob_idx]
        else: # otherwise return the most likely index
            max_prob_class = max_prob_idx
        
        return (max_prob_class, probs[max_prob_idx]) # returns most likely class and its probability


if __name__ == '__main__':
    n = NaiveBayesClassifier()
    n.get_raw_data()
    c = n.create_corpus()
    #print(c)
    est, vectorizer = n.training_pipeline(c)
    # print(n.raw_data)
    # print(type(n.raw_data["tokenized"][0]))
    auth, prob = n.classify_text("mamma ha detto di venirmi a prendere", est, vectorizer, labels=["Alex", "Kevin"])
    print(f"most likely author is {auth} \nwith probability {prob}")
