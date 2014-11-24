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


if __name__=='__main__':   #main function
	#movieids = defaultdict(string)
	html = ''
	for line in open('./movieIds.txt'):
		mId = line.strip().split('|')
		#movieids[mId[0]] = mId[1]
		print mId[1]
		print mId[0]
	#print html