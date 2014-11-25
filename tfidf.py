#!/usr/bin/env python
#The above line specifies to the Unix that the file is a python script 

"""
COMPUTATIONAL LINGUISTICS

Parses through summaries and texts of movie reviews and computes TFIDF scores for each word, stored in the tfidf.txt file
Improves speed in that TFIDF scores do not have to be computed each time the program is run, but instead can be read off from a file
"""

from __future__ import division          #integer division
from collections import defaultdict
import random
import string        #some string-related utilities
import sys        #for command-line args
import re    #for regular expressions
import os
import math

#do not use the following words/part-of-speech tags in generating the sentence
dontInclude = ["-RRB-", "-LRB-", "<br\xc2\xa0/>", "<p>"]

class TF_IDF:
    def __init__(self, docCounts):
        self.documentCounts = docCounts


"""
# Function: get_document_counts(rootdir, documentCounts)
# Input: rootdir: the data directory, containing folders for each productID and preprocessed data for each productID
        documentCounts: dictionary that maps each word to its TFIDF score (words in summaries are weighted higher than words in texts)
# Output: the number of summaries.txt or texts.txt documents for each product ID

# Description:  accumulates counts for each word in movie reviews, which will be normalized in the tfidf_counts method
"""
def get_document_counts(rootdir, documentCounts):
    numberDocuments = 0
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            #f = file.read()
            fileCount = defaultdict(int)
            pathName = os.path.join(subdir, file)
            if pathName.endswith('summaries.txt') or pathName.endswith('texts.txt'):
                if pathName.endswith('summaries.txt'):
                    alpha = 0.5 # constant for summaries
                else:
                    alpha = 1
                numberDocuments += 1
                f = open(pathName).read()
                for word in f.split():
                    fileCount[word] += 1
                for word in fileCount:
                    documentCounts[word] += 1*alpha                
    return numberDocuments

"""
# Function: tfidf_counts()
# Output: dictionary that maps each word to its TFIDF score

# Description: parses through summaries and texts of each movie review to compute TFIDF score of each word
"""
def tfidf_counts():  
    documentCounts = defaultdict(int)
    numberDocs = get_document_counts("./data", documentCounts)
    for word, count in documentCounts.iteritems():
        documentCounts[word] = str(math.log(numberDocs/count))
    return documentCounts

if __name__=='__main__':
	f = open('tfidf.txt', 'w+')
	counts = tfidf_counts()
	for key in counts:
		f.write(key + '|' + counts[key] + '\n')

	f.close()


