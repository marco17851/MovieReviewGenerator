from nltk.corpus import wordnet as wn
import nltk
import random

def get_similar(inp):
	phrase = nltk.word_tokenize(inp)
	sentence = nltk.pos_tag(phrase)

	for index, part in enumerate(sentence):
		if part[1] == 'NN' or part[1] == 'JJ' or part[1] == 'VB' \
			or part[1] == 'JJS':
			synsets = wn.synsets(part[0])
			if len(synsets) == 0:
				continue
			rand = random.randint(0, len(synsets)-1)
			word = synsets[rand]
			similar = word.lemmas()
			if len(similar) == 0:
				continue
			rand = random.randint(0, len(similar)-1)
			if rand == 0:
				continue
			sim = similar[rand].name()
			phrase[index] = sim

	output = ""
	for x in phrase:
		output += (x + " ")

	return output


if __name__ == '__main__':
	sentence = "You don't want to miss this amazing movie!"
	print get_similar(sentence)	