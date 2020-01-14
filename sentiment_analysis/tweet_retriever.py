# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 03:25:25 2019

@author: Ifara Joshua
"""
import tweepy
import csv

consumer_key = '' #Enter your consumer key
consumer_secret = '' #Enter your consumer secret
access_token = '' #Enter your access token
access_secret = '' #Enter your access secret

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)
no_of_tweets = 200
def get_tweets(query):
    query = query + " -filter:retweets"
    try:
        api.verify_credentials()
        print('Authentication OK')
    except:
        print('Error during Authentication')
    
    csvFile = open('tweets.csv', 'w')
    csvWriter = csv.writer(csvFile)
    print('Fetching tweets....')
    tweets = tweepy.Cursor(api.search, q=query, lang='en').items(no_of_tweets)
    print('Tweets fetching completed')
    print('Writing tweets to file....')
    for t in tweets:
        csvWriter.writerow([t.text.encode('utf-8')])
        
    
    print('Writing completed')
    csvFile.close()
    
