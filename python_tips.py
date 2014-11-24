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
import subprocess

#Metadata of your program
___author__ = 'Sravana Reddy'
__date__ = 'Sep 2014'
__version__ = '1'


def count_words(filename):
    """Read a file and count the frequency of each word"""
    if not os.path.exists('./data'):
        os.makedirs('./data')
    curr_dir = ""

    countsdict = defaultdict(int)
    count = 0
    f = open('test.txt', 'w+')
    f2 = open('test2.txt', 'w+')
    
    keepReadingTexts = True
    #defaultdict make a dictionary where all the values are ints, implicitly initializes every value to 0.
    #For a dictionary where values are lists and initial values are [], use defaultdict(list)
    #For set values, defaultdict(set)
    #For floats, defaultdict(float)
    
    readytobegin = False
    
    for line in open(filename):  #lazy reading
        #split along whitespace. To split along any other symbol, line.split(','), etc.
        if line.startswith('product/productId:'):
            productId = line[19:len(line) - 1]
            if productId != curr_dir:
                curr_dir = productId
                if not os.path.exists('./data/' + productId):
                    os.makedirs('./data/' + productId)
                f2 = open('./data/' + curr_dir + '/texts.txt', 'w+')
                f = open('./data/' + curr_dir + '/summaries.txt', 'w+')

        if line.startswith('review/text'):
            processText(line, f2)

        if line.startswith('review/summary'):
            count += 1
            processSummary(line, f)
            """if count == 8:
                keepReadingTexts = False"""
            if count == 10000:
                f.close()
                f2.close()
                break
    
    return countsdict

def processText(textLine, f):
    f.write(textLine[13:])

def processSummary(summaryLine, f):
    f.write(summaryLine[16:])
    print summaryLine

def annotate_pos(rootdir):
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            pathName = os.path.join(subdir, file)
            if pathName.endswith('texts.txt'):
                print pathName
                print os.path.join(subdir, 'pos.txt')
                subprocess.call(['./stanford-postagger-2014-10-26/stanford-postagger.sh', './stanford-postagger-2014-10-26/models/english-bidirectional-distsim.tagger', pathName, '>', os.path.join(subdir, 'pos.txt')])
            else:
                if os.path.exists(os.path.join(subdir, 'pos.txt')):
                    print 'hehe ' + os.path.join(subdir, 'pos.txt')

if __name__=='__main__':   #main function
    wordcounts = count_words('./movies.txt')   #filename is first parameter
    #annotate_pos('./data')

    
    