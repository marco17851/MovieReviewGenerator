#!/usr/bin/env python
#The above line specifies to the Unix that the file is a python script 

"""
COMPUTATIONAL LINGUISTICS

PYTHON TIPS AND TRICKS (Sep 17, 2014)
"""
from __future__ import division          #integer division
from collections import defaultdict
import random
import string        #some string-related utilities
import sys        #for command-line args
import re    #for regular expressions
import math

tfidf_pos_tags = ['NNP', 'VBZ', 'JJ', 'NN', 'VB', 'NNS', 'VBD', 'NNPS', 'VBG']


class SentScore:
    def __init__(self, s, v):
        self.sentence = s
        self.val = v

    def __lt__ (self, other):
        return self.val < other.val

    def __gt__ (self, other):
        return other.__lt__(self)

    def __eq__ (self, other):
        return self.val == other.val

    def __ne__ (self, other):
        return not self.__eq__(other)

def tfidf():
    tfidf_dict = defaultdict(float)
    for line in open('./tfidf.txt'):
        words = line.split('|')
        try:
            tfidf_dict[words[0]] = float(words[1].strip())
        except:
            continue
    return tfidf_dict

def score_by_tfidf(sent_scores):
    sent_scores = []
    #print tfidf_counts
    #print '--------------'
    for sent in sentences:
        tfidf_score = 0
        sent_words = sent.split()
        separated_pos_seq = separate_pos(pos_sequence)
        for i in range(len(separated_pos_seq)):
            if separated_pos_seq[i] in tfidf_pos_tags:
                #print 'word: ' + sent_words[i]
                #print 'tfidf_score: ' + str(tfidf_counts[sent_words[i]])
                tfidf_score += float(tfidf_counts[sent_words[i]])
        sent_scores.append(SentScore(sent, tfidf_score))
    sent_scores.sort(reverse=True)
    return sent_scores