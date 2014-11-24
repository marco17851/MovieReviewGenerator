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

def annotate_pos(rootdir):
    f = open('../pos_tagged_movies.txt', 'w+')
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            pathName = os.path.join(subdir, file)
            if pathName.endswith('texts.txt'):
                #print pathName
                print os.path.join(subdir, 'pos.txt')
                f.write(os.path.join(subdir, 'pos.txt'))
                f.write('\n')
                if not os.path.exists(os.path.join(subdir, 'pos.txt')) and not os.path.exists(os.path.join(subdir, 'pos.txt')):
                	subprocess.call(['./stanford-postagger.sh', './models/english-bidirectional-distsim.tagger', pathName], stdout=open(os.path.join(subdir, 'pos.txt'), 'w'))
                else:
                    if os.path.exists(os.path.join(subdir, 'pos.txt')):
                        print 'hehe ' + os.path.join(subdir, 'pos.txt')
    f.close()

if __name__=='__main__':   #main function
    #wordcounts = count_words('./movies.txt')   #filename is first parameter
    annotate_pos('../data')