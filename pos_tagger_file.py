from collections import defaultdict
import sys
import os

def get_Ems_Trans_Uni(folderpath):

	for ID in os.listdir(folderpath):

		parse_essayfile(folderpath+"/"+ID)
		
		emissions = {}
		transitions = {}
		if ID == "B000UGBOT0":
			break

		#go inside movie folder and obtain pos.txt
		if not os.path.exists(folderpath+"/"+ID+"/pos.txt"):
			continue
		for line in open(folderpath+"/"+ID+"/pos.txt"):
			x = 0
			words = line.strip().split(" ")
			pastT = []

			for piece in words:
				pieces = piece.split("_")

				if len(pieces) != 2:
					continue
				if x == 0:
					x+=1
					pastT = pieces[1]
				else:
					if pastT not in transitions:
						transitions[pastT] = defaultdict(int)
					else:
						transitions[pastT][pieces[1]] += 1
					pastT = pieces[1]

				if pieces[1] not in emissions:
					emissions[pieces[1]] = defaultdict(int)
					emissions[pieces[1]][pieces[0]] += 1
				else:
					emissions[pieces[1]][pieces[0]] += 1
	
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
	
	return (emissions, transitions)

def get_Ems_Trans_Bg(folderpath):

	for ID in os.listdir(folderpath):

		parse_essayfile(folderpath+"/"+ID)
		
		emissions = {}
		transitions = {}
		if ID == "B000UGBOT0":
			break
		
		#go inside movie folder and obtain pos.txt
		if not os.path.exists(folderpath+"/"+ID+"/pos.txt"):
			continue
		for line in open(folderpath+"/"+ID+"/pos.txt"):
			x = 0
			words = line.strip().split(" ")
			pastP = []
			pastE = []
			pastT = []
			for piece in words:
				pieces = piece.split("_")

				if len(pieces) != 2:
					continue

				if x < 1:
					pastP.append(pieces[1])
					pastE.append(pieces[0])
					pastT.append(pieces[1])

				else:

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
	
	return (emissions, transitions)
	
def get_Ems_Trans_Tr(folderpath):

	for ID in os.listdir(folderpath):

		parse_essayfile(folderpath+"/"+ID)
		
		emissions = {}
		transitions = {}
		if ID == "B000UGBOT0":
			break
		
		#go inside movie folder and obtain pos.txt
		if not os.path.exists(folderpath+"/"+ID+"/pos.txt"):
			continue
		for line in open(folderpath+"/"+ID+"/pos.txt"):
			x = 0
			words = line.strip().split(" ")
			pastP = []
			pastE = []
			pastT = []
			for piece in words:
				pieces = piece.split("_")

				if len(pieces) != 2:
					continue

				if x < 2:
					pastP.append(pieces[1])
					pastE.append(pieces[0])
					pastT.append(pieces[1])

				else:
					""" Trigram """
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

				x+=1
	
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
	
	return (emissions, transitions)

def get_Reviews_Arpa(folderpath):

	for ID in os.listdir(folderpath):

		#parse_essayfile(folderpath+"/"+ID)
		
		bigram_info = defaultdict(lambda: defaultdict(list))
		#if ID == "B0070225F4":
		#	break

		#go inside movie folder and obtain pos.txt
		if not os.path.exists(folderpath+"/"+ID+"/pos.txt"):
			continue
		for line in open(folderpath+"/"+ID+"/pos.txt"):
			x = 0
			review = line.strip().split(" ")
			past = "<s>"

			for piece in review:
				pieces = piece.split("_")
				bigram_info[past][pieces[1]].append(pieces[0])
				past = pieces[0]
	
		arpa = open(folderpath+"/"+ID+"/reviews.arpa", "w")
		for key in bigram_info:
			arpa.write(key + "\n")
			for pos in bigram_info[key]:
				arpa.write(pos + " |")
				for word in bigram_info[key][pos]:
					arpa.write(" " + word)
				arpa.write("\n")

		arpa.close()
	

def parse_essayfile(filename):
    essay = open(filename+"/texts.txt")
    #print filename
    array = []
    for line in essay:
        new = line.lower().strip().split(".")
        for x in new:
            if x == "" or x == " " or len(x) < 20:
                continue
            else:
                #print x.split()
                array.append(x.split())
    sentence_ids = defaultdict(list)
    for i in range(len(array)):
    	for word in array[i]:
    		if i not in sentence_ids[word]:
    			sentence_ids[word].append(i)

    f = open(filename+'/sentence_ids.txt', 'w+')
    for key in sentence_ids:
    	f.write(key + ': ')
    	for num in sentence_ids[key]:
    		f.write(str(num) + ' ')
    	f.write('\n')

    return array

if __name__ == "__main__":
	folderpath = sys.argv[1]

	get_Ems_Trans_Uni(folderpath)
	get_Ems_Trans_Bg(folderpath)
	get_Ems_Trans_Tr(folderpath)
	get_Reviews_Arpa(folderpath)
	#print transitions
	
	