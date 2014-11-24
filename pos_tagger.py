from collections import defaultdict
import sys
import os

def get_Ems_Trans(folderpath):
	emissions = {}
	transitions = {}
	r = 0
	for ID in os.listdir(folderpath):
		if ID == "B000UGBOT0":
			break

		#if r == 1:
		#	break
		#r+=1
		
		#go inside movie folder and obtain pos.txt
		for line in open(folderpath+"/"+ID+"/pos.txt"):
			x = 0
			words = line.strip().split(" ")

			pastP = [] #PartsOfSpeech
			pastE = [] #Emissions
			pastT = []

			for piece in words:
				pieces = piece.split("_")

				if len(pieces) != 2:
					continue

				""" Unigrams """	
				"""
				if x == 0:
					x+=1
					if "<s>" not in transitions:
						transitions["<s>"] = defaultdict(int)
					transitions["<s>"][pieces[1]] += 1
					pastT = pieces[1]
				else:
					if pastT not in transitions:
						transitions[pastT] = defaultdict(int)
					else:
						transitions[pastT][pieces[1]] += 1
					pastT = pieces[1]
				"""


				if x < 1:
					""" Trigram """
					pastP.append(pieces[1])
					pastE.append(pieces[0])
					pastT.append(pieces[1])
					
					
					""" Bigram
					if ("<s>_" + pieces[1]) not in emissions:
						emissions["<s>_" + pieces[1]] = defaultdict(int)
					emissions["<s>_" + pieces[1]]["<s>_" + pieces[0]] += 1
					pastP = pieces[1]
					pastE = pieces[0]
					"""

				else:
					""" Trigram 
					if (pastP[0] + "_" + pastP[1] + "_" + pieces[1]) not in emissions:
						emissions[pastP[0] + "_" + pastP[1] + "_" + pieces[1]] = defaultdict(int)
					emissions[pastP[0] + "_" + pastP[1] + "_" + pieces[1]][pastE[0] + "_" + pastE[1] + "_" + pieces[0]] += 1
					pastP.pop(0)
					pastP.append(pieces[1])
					pastT.append(pieces[1])
					pastE.pop(0)
					pastE.append(pieces[0])

					if x > 5:
						if (pastT[0] + "_" + pastT[1] + "_" + pastT[2]) not in transitions:
							transitions[pastT[0] + "_" + pastT[1] + "_" + pastT[2]] = defaultdict(int)
						transitions[pastT[0] + "_" + pastT[1] + "_" + pastT[2]][pastT[3] + "_" + pastT[4] + "_" + pastT[5]] += 1
						pastT.pop(0)
					"""


					""" Bigram """
					if (pastP[0] + "_" + pieces[1]) not in emissions:
						emissions[pastP[0] + "_" + pieces[1]] = defaultdict(int)
					emissions[pastP[0] + "_" + pieces[1]][pastE[0] + "_" + pieces[0]] += 1
					pastP.pop(0)
					pastP.append(pieces[1])
					pastT.append(pieces[1])
					pastE.pop(0)
					pastE.append(pieces[0])

					if x > 3:
						if (pastT[0] + "_" + pastT[1]) not in transitions:
							transitions[pastT[0] + "_" + pastT[1]] = defaultdict(int)
						transitions[pastT[0] + "_" + pastT[1]][pastT[2] + "_" + pastT[3]] += 1
						pastT.pop(0)

				x+=1
					
	
	ems = open("bg_emissions.txt", "w")
	trans = open("bg_transitions.txt", "w")
	for thing in emissions:
		ems.write(thing + "\n")
		for obs in emissions[thing]:
			ems.write(obs + "\t" + str(emissions[thing][obs]) + "\n")
	for thing in transitions:
		trans.write(thing + "\n")
		for obs in transitions[thing]:
			trans.write(obs + "\t" + str(transitions[thing][obs]) + "\n")
	
	return (emissions, transitions)
	


if __name__ == "__main__":
	folderpath = sys.argv[1]

	(emissions, transitions) = get_Ems_Trans(folderpath)
	#print transitions
	
	