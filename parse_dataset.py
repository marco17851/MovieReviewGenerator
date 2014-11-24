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

#filename is the dataset of Amazon reviews, consisting of summaries and texts for each movie review.
def compile_summaries_and_texts(filename):
    
    #Make a directory named "data", with subfolders for each product ID.
    if not os.path.exists('./data'):
        os.makedirs('./data')

    #curr_product tracks the current product ID as we read the data file line by line
    curr_product = ""

    #count is the number of movie reviews that have been processed so far
    count = 0

    #allsummaries.txt contains every movie review summary 
    allsummariesfile = open('allsummaries.txt', 'w+')

    #f and f2 are the texts and summaries files; initialize them to dummy values for now
    f = open('test.txt', 'w+')
    f2 = open('test2.txt', 'w+')
    
    for line in open(filename):
        #the data file is organized such that the first line for a movie review is the productID
        if line.startswith('product/productId:'):
            productId = line[19:len(line) - 1]

            #if the productID differs from curr_product, then the movie reviews for curr_product have all been parsed,
            #so update curr_product to be the next productID in the data set
            if productId != curr_product:
                curr_product = productId

                #create a directory for the product ID
                if not os.path.exists('./data/' + productId):
                    os.makedirs('./data/' + productId)

                #update f and f2 to be the texts and summaries file for the current product ID
                f2 = open('./data/' + curr_product + '/texts.txt', 'w+')
                f = open('./data/' + curr_product + '/summaries.txt', 'w+')

        #ach movie review has a summary section, the line for which begins with 'review/text'
        if line.startswith('review/summary'):
            processSummary(line, f)
            processSummary(line, allsummariesfile)

        #each movie review has a text section, the line for which begins with 'review/text'
        if line.startswith('review/text'):
            processText(line, f2)
            count += 1
            #if 10000 movie reviews have been processed, terminate the program
            if count == 10000:
                f.close()
                f2.close()
                break

#write the text for a movie review to the texts.txt file specified by f
def processText(textLine, f):
    f.write(textLine[13:])

#write the summary for a movie review to the summaries.txt file specified by f
def processSummary(summaryLine, f):
    f.write(summaryLine[16:])
    print summaryLine

if __name__=='__main__':   #main function
    compile_summaries_and_texts('./movies.txt') #./movies.txt is the data set file containing the Amazon reviews

    
    