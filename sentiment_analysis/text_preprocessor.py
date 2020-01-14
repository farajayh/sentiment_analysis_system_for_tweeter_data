# -*- coding: utf-8 -*-
"""
Created on Sun Oct 20 19:58:23 2019

@author: Ifara Joshua
"""

import re
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
import nltk

from stemming.porter2 import stem

def remove_pattern(input_txt, pattern):
    r = re.findall(pattern, input_txt)
    for i in r:
        input_txt = re.sub(i, '', input_txt)
        
        
    return input_txt


def get_pos(word):
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {'J' :wordnet.ADJ, 'N':wordnet.NOUN, 'V':wordnet.VERB, 'R':wordnet.ADV}
    return tag_dict.get(tag, wordnet.NOUN)

def clean(text):
    text = text.lower() #convert to lower case
    text = remove_pattern(text, '@[\w]*') #remove @user 
    text = re.sub('[^a-zA-Z# \n\.]', '', text) #remove special characters
    text = re.sub(r'http\S+|www\S+|ftp://\S+', ' ', text) #remove url
    
    return text

def preprocess(text):
    text = text.lower() #convert to lower case
    text = remove_pattern(text, '@[\w]*') #remove @user 
    text = re.sub('[^a-zA-Z# \n\.]', '', text) #remove special characters
    text = re.sub(r'http\S+|www\S+|ftp://\S+', ' ', text) #remove url
    text = " ".join(stem(w) for w in nltk.word_tokenize(text)) #tokenization and stemming
    
    
    return text
    