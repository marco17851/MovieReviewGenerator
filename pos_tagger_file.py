# coding: utf-8
"""
# Authors: 	Marco Barragan, Barry Chen
# Date: 	November 16, 2014

# Input: 	Takes in the root folder path for the data files.
# Output: 	It outputs 7 different files for each movie.
			1) The unigram emissions and transitions.
			2) The bigram emissions and transitions.
			3) The trigram emissions and transitions.
			4) The reviews.arpa file which contains words and 
				their part of speech transitions for that movie.

# Description:	This program reads the part of speech text file that contains
				the movie reviews and the parts of speech that go with each
				word in the review.
				Then, it obtains the unigrams, the bigrams, and the trigrams
				from each movie file.
				Afterwards, it creates the text files that contain the
				information mentioned above as well as the reviews.arpa file.
"""
# coding=utf-8
from collections import defaultdict
import sys
import os


"""
# Function: get_Ems_Trans_Uni()
# Input: folderpath = the root path for the data
# Output: the text files containing the unigrams emission and transitions.
			|| emissions.txt || transitions.txt ||

# Description: 	Obtains the unigrams for the emissions and transitions
				from each movie file.
"""
def get_Ems_Trans_Uni(folderpath):

	dontInclude = ["-RRB-", "-LRB-", "<br />"]

	# Loops through the data folder
	for ID in os.listdir(folderpath):

		parse_essayfile(folderpath+"/"+ID)
		
		# Dictionary for the emissions and transitions
		emissions = {}
		transitions = {}

		# Stops at movie #~300
		if ID == "B000UGBOT0":
			break

		# Go inside movie folder and obtain pos.txt
		if not os.path.exists(folderpath+"/"+ID+"/pos.txt"):
			continue
		for line in open(folderpath+"/"+ID+"/pos.txt"):
			x = 0
			words = line.strip().split(" ")
			pastT = []

			# Loops through the words and their part of speech
			for piece in words:
				pieces = piece.split("_")

				# If the word does not have a part of speech, disregard it
				if len(pieces) != 2:
					continue

				if pieces[0] in dontInclude or pieces[1] in dontInclude:
					continue

				# Updates the unigram transitions/frequencies based on 
				# the past and current word
				if x == 0:
					x+=1
					pastT = pieces[1]
				else:
					if pastT not in transitions:
						transitions[pastT] = defaultdict(int)
					else:
						transitions[pastT][pieces[1]] += 1
					pastT = pieces[1]

				# Updates the unigram emissions/frequencies based on 
				# the part of speech and current word
				if pieces[1] not in emissions:
					emissions[pieces[1]] = defaultdict(int)
					emissions[pieces[1]][pieces[0]] += 1
				else:
					emissions[pieces[1]][pieces[0]] += 1
	
		# Writes to the files the emissions and transitions of that movie
		ems = open(folderpath+"/"+ID+"/emissions.txt", "w")
		trans = open(folderpath+"/"+ID+"/transitions.txt", "w")
		for thing in emissions:
			ems.write(thing + "\n")
			for obs in emissions[thing]:
				ems.write(obs + "\t" + str(emissions[thing][obs]) + "\n")
		for thing in transitions:
			trans.write(thing + "\n")
			for obs in transitions[thing]:
				trans.write(obs + "\t" + str(transitions[thing][obs]) + "\n")

		ems.close()
		trans.close()


"""
# Function: get_Ems_Trans_Bg()
# Input: folderpath = the root path for the data
# Output: the text files containing the bigram emission and transitions.
			|| bg_emissions.txt || bg_transitions.txt ||

# Description: 	Obtains the bigrams for the emissions and transitions
				from each movie file.
"""
def get_Ems_Trans_Bg(folderpath):

	# Loops through the directory that contains the movie files
	for ID in os.listdir(folderpath):

		parse_essayfile(folderpath+"/"+ID)
		
		# The dictionaries for the emissions and transitions
		emissions = {}
		transitions = {}
		if ID == "B000UGBOT0":
			break
		
		# Go inside movie folder and obtain pos.txt
		if not os.path.exists(folderpath+"/"+ID+"/pos.txt"):
			continue
		for line in open(folderpath+"/"+ID+"/pos.txt"):
			x = 0

			words = line.strip().split(" ")
			pastP = []		# Past Part of Speech Tags
			pastE = []		# Past Emissions
			pastT = []		# Past Transitions

			# Loops through the words in the reviews
			for piece in words:
				pieces = piece.split("_")

				if len(pieces) != 2:
					continue

				# Appends the previous word / POS tag
				if x < 1:
					pastP.append(pieces[1])
					pastE.append(pieces[0])
					pastT.append(pieces[1])

				else:
					# Updates the emissions based on the previous POS tag
					# and the current emission
					if (pastP[0] + "_" + pieces[1]) not in emissions:
						emissions[pastP[0] + "_" + pieces[1]] = defaultdict(int)
					emissions[pastP[0] + "_" + pieces[1]][pastE[0] + "_" + pieces[0]] += 1
					pastP.pop(0)
					pastP.append(pieces[1])
					pastT.append(pieces[1])
					pastE.pop(0)
					pastE.append(pieces[0])

					# Updates the bigram transitions based on the previous two
					# transitions and the current two
					if x > 3:
						if (pastT[0] + "_" + pastT[1]) not in transitions:
							transitions[pastT[0] + "_" + pastT[1]] = defaultdict(int)
						transitions[pastT[0] + "_" + pastT[1]][pastT[2] + "_" + pastT[3]] += 1
						pastT.pop(0)

				x+=1
	
		# Writes to the appropriate files, the bigram emissions and transitions
		ems = open(folderpath+"/"+ID+"/bg_emissions.txt", "w")
		trans = open(folderpath+"/"+ID+"/bg_transitions.txt", "w")
		for thing in emissions:
			ems.write(thing + "\n")
			for obs in emissions[thing]:
				ems.write(obs + "\t" + str(emissions[thing][obs]) + "\n")
		for thing in transitions:
			trans.write(thing + "\n")
			for obs in transitions[thing]:
				trans.write(obs + "\t" + str(transitions[thing][obs]) + "\n")

		ems.close()
		trans.close()
	

"""
# Function: get_Ems_Trans_Tr()
# Input: folderpath = the root path for the data
# Output: the text files containing the trigram emission and transitions.
			|| tr_emissions.txt || tr_transitions.txt ||

# Description: 	Obtains the trigrams for the emissions and transitions
				from each movie file.
"""
def get_Ems_Trans_Tr(folderpath):

	# Loops through the directory that contains the movie files
	for ID in os.listdir(folderpath):

		parse_essayfile(folderpath+"/"+ID)
		
		# Dictionaries for the emissions and transitions
		emissions = {}
		transitions = {}
		if ID == "B000UGBOT0":
			break
		
		#go inside movie folder and obtain pos.txt
		if not os.path.exists(folderpath+"/"+ID+"/pos.txt"):
			continue

		# Loops through the lines in the part of speech text files
		for line in open(folderpath+"/"+ID+"/pos.txt"):
			x = 0

			words = line.strip().split(" ")
			pastP = []		# Past Part of Speech Tags
			pastE = []		# Past Emissions
			pastT = []		# Past Transitions

			# Loops through the words in the reviews
			for piece in words:
				pieces = piece.split("_")

				if len(pieces) != 2:
					continue

				# Appends the first two words/POS tags
				if x < 2:
					pastP.append(pieces[1])
					pastE.append(pieces[0])
					pastT.append(pieces[1])

				else:
					""" Trigram """
					# Updates the emissions based on the emissions and their POS tags
					if (pastP[0] + "_" + pastP[1] + "_" + pieces[1]) not in emissions:
						emissions[pastP[0] + "_" + pastP[1] + "_" + pieces[1]] = defaultdict(int)
					emissions[pastP[0] + "_" + pastP[1] + "_" + pieces[1]][pastE[0] + "_" + pastE[1] + "_" + pieces[0]] += 1
					pastP.pop(0)
					pastP.append(pieces[1])
					pastT.append(pieces[1])
					pastE.pop(0)
					pastE.append(pieces[0])

					if x > 5:
						# Updates the transitions based on the previous 3 transitions
						# and the current 3 transitions
						if (pastT[0] + "_" + pastT[1] + "_" + pastT[2]) not in transitions:
							transitions[pastT[0] + "_" + pastT[1] + "_" + pastT[2]] = defaultdict(int)
						transitions[pastT[0] + "_" + pastT[1] + "_" + pastT[2]][pastT[3] + "_" + pastT[4] + "_" + pastT[5]] += 1
						pastT.pop(0)

				x+=1
	
		# Writes the information to the emissions and transitions files
		ems = open(folderpath+"/"+ID+"/tr_emissions.txt", "w")
		trans = open(folderpath+"/"+ID+"/tr_transitions.txt", "w")
		for thing in emissions:
			ems.write(thing + "\n")
			for obs in emissions[thing]:
				ems.write(obs + "\t" + str(emissions[thing][obs]) + "\n")
		for thing in transitions:
			trans.write(thing + "\n")
			for obs in transitions[thing]:
				trans.write(obs + "\t" + str(transitions[thing][obs]) + "\n")

		ems.close()
		trans.close()


"""
# Function: get_Reviews_Arpa()
# Input: folderpath = the root path for the data
# Output: the text files containing a word, the following POS tag, and
			the words of that POS tag.
			For example:
			ate
			DT|the a an

# Description: 	Obtains the bigram arpa information from the reviews.
"""
def get_Reviews_Arpa(folderpath):

	# Loops through the root directory
	for ID in os.listdir(folderpath):

		#parse_essayfile(folderpath+"/"+ID)
		
		# The dictionary containing the bigrams
		bigram_info = defaultdict(lambda: defaultdict(list))

		# Go inside movie folder and obtain pos.txt
		if not os.path.exists(folderpath+"/"+ID+"/pos.txt"):
			continue
		for line in open(folderpath+"/"+ID+"/pos.txt"):
			x = 0
			review = line.strip().split(" ")
			past = "<s>"

			# Obtains the past word and appends the current word
			# given the current word's POS tag
			for piece in review:
				pieces = piece.split("_")
				bigram_info[past][pieces[1]].append(pieces[0])
				past = pieces[0]
	
		# Writes the information to the appropriate file
		arpa = open(folderpath+"/"+ID+"/reviews.arpa", "w")
		for key in bigram_info:
			arpa.write(key + "\n")
			for pos in bigram_info[key]:
				arpa.write(pos + " |")
				for word in bigram_info[key][pos]:
					arpa.write(" " + word)
				arpa.write("\n")

		arpa.close()
	
"""
# Function: parse_essayfile()
# Input: filename = the name of the file that will be parsed
# Output: the text file containing the word and the sentence it is found in

# Description: 	Parses the review files in order to obtain the word and
				the sentence it is found in. This will be used when we
				generate sentences as we might want to get words from
				sentences that are close to each other/from the same sentence.
"""
def parse_essayfile(filename):
    essay = open(filename+"/texts.txt")
    #print filename
    array = []

    # Loops through each line and obtains the splitted lines
    # and then appends the words
    for line in essay:
        new = line.lower().strip().split(".")
        for x in new:
            if x == "" or x == " " or len(x) < 20:
                continue
            else:
                #print x.split()
                array.append(x.split())

    # Obtains the sentence IDs for each word
    sentence_ids = defaultdict(list)
    for i in range(len(array)):
    	for word in array[i]:
    		if i not in sentence_ids[word]:
    			sentence_ids[word].append(i)

    # Writes the information to the output file
    f = open(filename+'/sentence_ids.txt', 'w+')
    for key in sentence_ids:
    	f.write(key + ': ')
    	for num in sentence_ids[key]:
    		f.write(str(num) + ' ')
    	f.write('\n')


if __name__ == "__main__":
	folderpath = sys.argv[1]

	get_Ems_Trans_Uni(folderpath)
	get_Ems_Trans_Bg(folderpath)
	get_Ems_Trans_Tr(folderpath)
	get_Reviews_Arpa(folderpath)
	
	