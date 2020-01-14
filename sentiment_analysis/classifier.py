# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 22:40:19 2019

@author: Ifara Joshua
"""

import numpy as np
import pandas as pd
from text_preprocessor import *
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.metrics import accuracy_score, classification_report
from sklearn.pipeline import Pipeline
import pickle


tweet_data = pd.read_csv('main_data.csv')
tweet_data = tweet_data.drop_duplicates(['TweetText'])
tweet_data = tweet_data.fillna(value=' ')
tweet_data['tidy_tweets'] = np.vectorize(preprocess)(tweet_data['TweetText'])

tfidf_vectorizer = TfidfVectorizer(max_df=0.90, min_df=2, max_features=5000, ngram_range=(1,1))
tfidf = tfidf_vectorizer.fit_transform(tweet_data['tidy_tweets'])
pickle.dump(tfidf_vectorizer, open('vectorizer.pkl', 'wb'))

x_train, x_test, y_train, y_test = train_test_split(tfidf, tweet_data['Sentiment'], test_size=0.2, random_state=2)
model = svm.SVC(kernel='linear', C=3.0)
model.fit(x_train, y_train)

predictions = model.predict(x_test)

print(classification_report(y_test, predictions)) 
print('Accuracy = ', accuracy_score(y_test, predictions))

pickle.dump(model, open('svm_classifier.pkl', 'wb'))