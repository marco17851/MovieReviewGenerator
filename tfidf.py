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
import os
import math

class TF_IDF:
    def __init__(self, docCounts):
        self.documentCounts = docCounts

def build_POS_table(posFile):
    f = open(posFile).read()
    posTable = []
    total_sequence = []
    for word in f.split():
        tags = word.split("_")
        if tags[1] is "." or tags[1] is "!" or tags[1] is "?":
            posTable.append(total_sequence)
            total_sequence = []
        else:
            total_sequence.append(tags[1])
    return posTable

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
