""" Student Name: AliQannan 
    Student ID : 120240154 """ 


import string
from collections import defaultdict, Counter

class SmartTextAnalyzer:
    def __init__(self):
        self.text = []# adding all words in file in list 
        self.sentences = [] # all sentences 
        self.word_counts = Counter()# make count for all words
        self.char_counts = Counter()# make count for all char
        self.vocabulary = set()
        self.stop_words = {'the', 'a', 'is', 'and', 'of', 'to', 'in'}
        self.bigrams = defaultdict(Counter)# make sure I don't have missing keys
        self.positive_words = {'good', 'happy', 'great', 'excellent', 'love', 'wonderful'}
        self.negative_words = {'bad', 'sad', 'terrible', 'awful', 'hate', 'horrible'}

   