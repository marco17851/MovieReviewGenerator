"""
# Authors: 	Marco Barragan
# Date: 	November 15, 2014

# Input: 	None
# Output: 	A sentence similar to "You don't want to miss this amazing movie!"

# Description: 	This program was written to test out Wordnet and how to use it.
				It isn't necessary for the program as a whole.
"""

from nltk.corpus import wordnet as wn
import nltk
import random

"""
# Function: get_similar()
# Input: inputPhrase = the phrase that will be modified
# Output: a similar sentence to the phrase that was inputed

# Description: 	Uses Wordnet to obtain synonyms/similar words to the
				Nouns, Verbs, and Adjectives in a sentence.
"""
def get_similar(inputPhrase):

	phrase = nltk.word_tokenize(inputPhrase)
	sentence = nltk.pos_tag(phrase)

	# Loops through the words and tags in the sentence
	for index, part in enumerate(sentence):

		# If the tag is a noun, adjective, or verb, obtain a similar word
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

	# Outputs the similar sentence with the words replaced
	output = ""
	for x in phrase:
		output += (x + " ")

	return output


if __name__ == '__main__':
	sentence = "You don't want to miss this amazing movie!"
	print get_similar(sentence)	