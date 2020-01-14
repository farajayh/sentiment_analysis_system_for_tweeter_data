# -*- coding: utf-8 -*-
"""
Created on Sat Oct 26 19:02:07 2019

@author: Ifara Joshua
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from text_preprocessor import *
from tweet_retriever import *
import pickle
from flask import Flask, request, jsonify, render_template
import base64
from io import BytesIO

app = Flask(__name__)
model = pickle.load(open('svm_classifier.pkl', 'rb'))
tfidf_vectorizer = pickle.load(open('vectorizer.pkl', 'rb'))

def predictor(tweet_query):
    tweet_query = [tweet_query]
    tfidf = tfidf_vectorizer.transform(tweet_query)
    prediction = model.predict(tfidf)
    return prediction[0]

def show_wordcloud(words):
    wordcloud = WordCloud(width=800, height=500, random_state=21, max_font_size=110).generate(words)
    plt.figure(figsize=(10, 7))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis('off')
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    cloud_img = base64.b64encode(figfile.getvalue()).decode('ascii')
    plt.close()
    return cloud_img
    
@app.route('/')
@app.route('/index')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    tweet_query = request.form['query']
    #get_tweets(tweet_query)
    tweets = pd.read_csv('tweets.csv', header=None)     
    tweets = tweets.drop_duplicates([0])
    tweets = tweets.dropna()
    all_words = ' '.join([clean(text) for text in tweets[0]])
    tweets.to_csv('new_result.csv', index=False)
    tweets[0] = np.vectorize(preprocess)(tweets[0])
    tweet_cloud = show_wordcloud(all_words)
    tweets[1] = np.vectorize(predictor)(tweets[0])
    positive = len(tweets[tweets[1] == 'positive'])
    negative = len(tweets[tweets[1] == 'negative'])
    neutral = len(tweets[tweets[1] == 'neutral'])
    irrelevant = len(tweets[tweets[1] == 'irrelevant'])
    total = len(tweets[0])
    x = ['Positive', 'Negative', 'Nuetral', 'Irrelevant']
    y = [positive, negative, neutral, irrelevant]
    labels = [x[i] for i in range(4) if y[i] != 0]
    values = [i for i in y if i != 0]
    explode_val = [0 for i in values]
    max_val = max(values)
    for i in range(len(values)):
        if values[i] == max_val:
            explode_val[i] = 0.1
                       
    explode = tuple(explode_val)

    plt.figure(figsize=(10, 7))
    plt.bar(x,y)
    
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    barplot = base64.b64encode(figfile.getvalue()).decode('ascii')
    plt.close()
    
    fig1, ax1 = plt.subplots()
    ax1.pie(values, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
    
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    pieplot = base64.b64encode(figfile.getvalue()).decode('ascii')
    plt.close()
    tweets.to_csv('new_result.csv', index=False)
    results = True
    output = [total, positive, negative, neutral, irrelevant]
    plots = [tweet_cloud, barplot, pieplot]
    return render_template('index.html', results=results, output=output, plots=plots)

if __name__ == '__main__':
    app.run(debug=True)
    