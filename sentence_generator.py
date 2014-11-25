# coding: utf-8
#!/usr/bin/env python
#The above line specifies to the Unix that the file is a python script 

"""
# Authors:  Marco Barragan, Barry Chen
# Date:     November 16, 2014

Command to run program:
python sentence_generator.py [Product ID] [Movie Name] [Type of Review] [Type of Part-of-speech Template] [Word Choice Selection Method]

# Input:    Product ID: specifies the movie for which a review will be generated
            Movie Name: Title of the movie (to be printed out, not actually used in generating review)
            Type of Review: 
                0: extract a set of sentences from user reviews that most closely matches review summaries
                1: construct a computer-generated review
            Type of Part-of-speech Template
                0: randomly generate part-of-speech template based on an FSA
                1: select a sentence from the review to use as the part-of-speech template
            Word Choice Selection Method
                0: select contiguous groups of words from user reviews for each triplet of part-of-speech tags
                1: select one word at a time for each part-of-speech, using a bigram model based on the part-of-speech of the previous word

# Output:   A set of sentences for a movie based on the command-line specifications

# Description:  For extracting sentences directly from user reviews, refer to the ngram.py file.
            For computer-generated reviews, words from user reviews are selected for each part-of-speech in a part-of-speech template.
"""

from __future__ import division          #integer division
from collections import defaultdict
import random
import string        #some string-related utilities
import sys        #for command-line args
import re    #for regular expressions
import os
import math
import ngram

#Metadata of your program
___author__ = 'Sravana Reddy'
__date__ = 'Sep 2014'
__version__ = '1'
tolerance = 3
posEmissions = defaultdict(list)
bgPosEmissions = defaultdict(list)
uniPosEmissions = defaultdict(list)
tfidf_pos_tags = ['NNP', 'VBZ', 'JJ', 'NN', 'VB', 'NNS', 'VBD', 'NNPS', 'VBG']

#do not use the following words/part-of-speech tags in generating the sentence
dontInclude = ["-RRB-", "-LRB-", "<br\xc2\xa0/>", "<p>"]

"""
Inner class to compare two sentences (based on perplexity, TFIDF score, or some other measure)
"""
class SentScore:
    def __init__(self, s, v):
        self.sentence = s
        self.val = v

    def __lt__ (self, other):
        return self.val < other.val

    def __gt__ (self, other):
        return other.__lt__(self)

    def __eq__ (self, other):
        return self.val == other.val

    def __ne__ (self, other):
        return not self.__eq__(other)

"""
# Function: build_POS_table(posFile)
# Input: posFile = an annotated text file with part-of-speech tags (named pos.txt)
# Output: a list of part-of-speech sequences, each corresponding to a sentence in posFile

# Description:  Obtains a set of part-of-speech templates used to generate sentences
"""
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
            if tags[0] in dontInclude or tags[1] in dontInclude:
                continue
            else:
                total_sequence.append(tags[1])
    return posTable

"""
# Function: build_Probabilistic_POS(posFile, transitions)
# Input: posFile = an annotated text file with part-of-speech tags (named pos.txt)
            transitions = a file (named bg_transitions.txt) consisting of transition frequencies for part-of-speech sequences

# Output: a list of part-of-speech sequences

# Description: Obtains a set of part-of-speech templates by doing the following:

                Among the part-of-speech bigrams that start with DT, select one
                Probabilistically generate next part-of-speech using transition probabilities
                If you reach a "." part-of-speech, terminate the part-of-speech sequence there.
                Keep the sentence under like 20 part-of-speeches
"""
def build_Probabilistic_POS(posFile, transitions):
    """Note: Do not include part-of-speeches that are in the dontInclude global array. I'm not sure if Marco has already
        filtered those out from the transitions file..."""
    return [['DT', 'JJ', 'NN']]

"""
# Function: tfidf()
# Output: dictionary that maps each word to its TFIDF score

# Description: uses precomputed TFIDF scores from a text file to generate the dictionary to improve speed
"""
def tfidf():
    tfidf_dict = defaultdict(float)
    for line in open('./tfidf.txt'):
        words = line.split('|')
        try:
            tfidf_dict[words[0]] = float(words[1].strip())
        except:
            continue
    return tfidf_dict

"""
Inner class to store a word and its frequency, used for computing emission probabilities
"""
class WordFreq:
    def __init__(self, w, f):
        self.word = w
        self.freq = f

    def __repr__(self):
        return '(' + self.word + ' ' + str(self.freq) + ')'

"""
# Function: populateDicts(filename, productID, emissions)
# Input: filename: text file containing words for each part-of-speech category and the frequencies of each word (i.e. emissions.txt)
        productID: the product ID specifying the movie reviews that the emission probabilities are based on
        emissions: a dictionary: key is part-of-speech, value is array of WordFreq

# Description: a function that populates unigram, bigram, or trigram emission dictionaries (which are global variables)
            Dictionary looks like: {'Det' -> [('the', 0.3), ('a', 0.7)], 'ADJ' -> [('red', 0.5), ('yellow', 0.5)]}
"""
def populateDicts(filename, productID, emissions):
    currPOS = ""

    for line in open('./data/' + productID + filename):
        words = line.split()
        if len(words) == 1:
            currPOS = words[0]
            continue
        emissions[currPOS].append(WordFreq(words[0], float(words[1])))

    for key in emissions:
        total = 0
        for wordfreq in emissions[key]:
            total += wordfreq.freq
        for i in range(len(emissions[key])):
            emissions[key][i].freq = emissions[key][i].freq/total

"""
# Function: transitions(productID)
# Input: productID: the product ID specifying the movie reviews that the transition probabilities are based on
# Output: returns a nested dictionary that specifies for each word, the part-of-speeches that follow that word, 
            and the words belonging to that part-of-speech
        Example: {'The' -> {'ADJ' -> ['red', 'yellow']}, 'red' -> {'NN' -> ['car', 'house']}}

# Description: the transition probabilities are used to determine each subsequent word in the computer-generated sentence
            using a bigram model based on the previous word
"""
def transitions(productID):
    arpa_dict = defaultdict(lambda: defaultdict(list))
    curr_key = ''
    for line in open('./data/' + productID + '/reviews.arpa'):
        words = line.split('|')
        if len(words) == 1:
            curr_key = words[0].strip()
            continue
        for w in words[1].split():
            arpa_dict[curr_key][words[0].strip()].append(w.strip())
    return arpa_dict

"""
# Function: getWordFromUnigramEmissions(ID, pos)
# Input: ID: Product ID specifying the reviews from which to select the word
        pos: the part of speech of the returned word

# Description: given a product ID, select any word that has the right part of speech given by pos
"""
def getWordFromUnigramEmissions(ID, pos):
    array = []
    found = 0

    file = open("./data/" + ID + "/emissions.txt")

    for line in file:
        words = line.strip().split("\t")

        if words[0] == pos and len(words) == 1:
            found = 1
            continue
        if len(words) == 2 and found == 0:
            continue
        if len(words) == 1 and found == 0:
            continue
        if found == 1 and len(words) == 1:
            break
        for x in range (0, int(words[1])):
            array.append(words[0])

    rand = 0
    try:
        rand = random.randint(0, len(array)-1)
    except:
        if len(array) == 0:
            return "..."

    return array[rand]

"""
# Function: sentenceBigrams(productID, tfidf_counts, pos_sequence)
# Input: productID: the product ID specifying which movie to generate sentences for
        tfidf_counts: dictionary: key is a word, and value of the word's TFIDF score
        pos_sequence: part-of-speech template for the sentence
# Output: returns a set of sentences for a movie product ID

# Description: generates a set of sentences using a part-of-speech template
            To generate the next word in a sentence, find the part-of-speeches that follow the current word and select one,
            and then select a word for that part-of-speech
"""
def sentenceBigrams(productID, tfidf_counts, pos_sequence):

    sentences = []
    arpa_dict = transitions(productID)

    for i in range(10):

        sentence = ''
        curr_key = '<s>'
        pos_seq_feasible = True

        for pos in pos_sequence:
            words = arpa_dict[curr_key][pos]
            if len(words) == 0:
                selected_word = getWordFromUnigramEmissions(productID, pos)
                curr_key = selected_word
                sentence += selected_word + ' '
            else:
                x = random.randint(0,len(words) - 1)
                sentence += words[x] + ' '
                curr_key = words[x]

        if pos_seq_feasible == True:
            sentences.append(sentence)

    sent_scores = []

    for sent in sentences:
        tfidf_score = 0
        sent_words = sent.split()

        for i in range(len(pos_sequence)):
            if pos_sequence[i] in tfidf_pos_tags:
                tfidf_score += float(tfidf_counts[sent_words[i]])
        sent_scores.append(SentScore(sent, tfidf_score))
    
    sent_scores.sort(reverse=True)

    best_sentences = []
    for i in range(min( len(sent_scores), 1)):
        best_sentences.append(sent_scores[i].sentence)
    return best_sentences

"""
# Function: sentence(productID, tfidf_counts, pos_sequence)
# Input: productID: the product ID specifying which movie to generate sentences for
        tfidf_counts: dictionary: key is a word, and value of the word's TFIDF score
        pos_sequence: part-of-speech template for the sentence
# Output: returns a set of sentences for a movie product ID

# Description: generates a set of sentences based on a part-of-speech template by selecting words
            three at a time for each part-of-speech triplet (but overlap the triplets)

        How it works:
            POS Template: "DET" "ADJ" "NN" "PRP" "DET" "NN"
            Generate three words for "DET" "ADJ" "NN", i.e. "the red house"
            Generate three words for "NN" "PRP" "DET", i.e. "car in the"
            Generate two words for "DET" "NN", i.e. "a neighborhood"

        Generated sentence: the red house in the neighborhood

        Finally, scores each sentence using TFIDF, and returns the sentence with the highest score
"""
def sentence(productID, tfidf_counts, pos_sequence):

    populateDicts('/tr_emissions.txt', productID, posEmissions)
    populateDicts('/bg_emissions.txt',productID, bgPosEmissions)
    populateDicts('/emissions.txt',productID, uniPosEmissions)        

    sentences = []
    for i in range(10):
        computed_sent = generateSentence(pos_sequence, posEmissions)
        if computed_sent == None:
            return None
        sentences.append(computed_sent)

    sent_scores = []
    for sent in sentences:
        tfidf_score = 0
        sent_words = sent.split()
        separated_pos_seq = separate_pos(pos_sequence)
        for i in range(len(separated_pos_seq)):
            if separated_pos_seq[i] in tfidf_pos_tags:
                tfidf_score += float(tfidf_counts[sent_words[i]])
        sent_scores.append(SentScore(sent, tfidf_score))
    sent_scores.sort(reverse=True)

    best_sentences = []
    for i in range(min( len(sent_scores), 1)):
        best_sentences.append(sent_scores[i].sentence)
    return best_sentences

"""
# Function: separate_pos(pos_sequence)
# Input: pos_sequence: part-of-speech template as triplets
# Output: returns a sequence of unigram part of speeches

# Description: converts a pos-sequence like ["DET_ADJ_NN", "PRP_DET_NN"] to ["DET", "ADJ", "NN", "PRP", "DET", "NN"]
                serves as a helper method for overlapping the part-of-speech tags
"""
def separate_pos(pos_sequence):
    pos_seq = []
    for pos in pos_sequence:
        for p in pos.split('_'):
            pos_seq.append(p)

    return pos_seq

"""
# Function: overlap(pos_sequence)
# Input: pos_sequence: part-of-speech template as triplets
# Output: returns a sequence of unigram part of speeches

# Description: converts a pos-sequence like ["DET_ADJ_NN", "PRP_DET_NN"] to ["DET", "ADJ", "NN", "PRP", "DET", "NN"]
                serves as a helper method for overlapping the part-of-speech tags
"""
def overlap(pos_sequence):
    #print pos_sequence
    overlapping_pos_seq = []

    unigram_pos_seq = separate_pos(pos_sequence)

    curr_pos_seq = ''
    for i in range(len(unigram_pos_seq)):
        if (i - 2) % 2 == 0 and i >= 2:
            curr_pos_seq += unigram_pos_seq[i]
            overlapping_pos_seq.append(curr_pos_seq)
            curr_pos_seq = unigram_pos_seq[i] + '_'
        elif i == len(unigram_pos_seq) - 1 and len(curr_pos_seq) != 0:
            curr_pos_seq += unigram_pos_seq[i]
            overlapping_pos_seq.append(curr_pos_seq)
            continue
        else:
            curr_pos_seq += unigram_pos_seq[i] + '_'
    #print overlapping_pos_seq
    return overlapping_pos_seq

"""
# Function: generateSentence(pos_sequence, posEmissions)
# Input: pos_sequence: part-of-speech template as triplets
        posEmissions: a dictionary: key is part-of-speech triplet, value is array of WordFreq consisting of three-word-sequences
            that adhere to the part-of-speech triplet, along with their frequences
# Output: returns a single sentence generated probabilistically based on posEmissions that adheres to the pos_sequence template
"""
def generateSentence(pos_sequence, posEmissions):
    sentence = ""
    print pos_sequence
    pos_sequence = overlap(pos_sequence)

    first_pos = True

    for pos in pos_sequence:
        #generate a random number between 0 and 1, representing which trigram to select
        rand_num = random.random()
        
        #if pos is not in posEmissions, then pos is a bigram or unigram part-of-speech sequence
        if pos not in posEmissions:            
            wordsToAdd = []
            if len(pos.split('_')) == 2:
                for word in bgPosEmissions[pos][0].word.split('_'):
                    wordsToAdd.append(word)

            if len(pos.split('_')) == 1:
                for word in uniPosEmissions[pos][0].word.split('_'):
                    wordsToAdd.append(word)
            if first_pos == True:
                first_pos = False
                for word in wordsToAdd:
                    sentence += word + ' '
            else:
                for word in wordsToAdd[1:]:
                    sentence += word + ' '
            continue

        for i in range(0, len(posEmissions[pos])):
            rand_num -= posEmissions[pos][i].freq
            if rand_num < 0:
                words = posEmissions[pos][i].word.split("_")

                if first_pos == True:
                    first_pos = False
                else:
                    words = words[1:]

                if words[0] == "<s>":
                    for y in range(1, len(words)):
                        sentence += words[y] + ' '
                else:
                    for y in range(0, len(words)):
                        sentence += words[y] + ' '
                break
    print sentence
    return sentence

"""
# Function: trigramify_pos_seq(pos_seq)
# Input: pos_seq: part-of-speech template
        
# Output: returns the part-of-speech sequence as triplets, with perhaps a unigram or bigram part-of-speech sequence at the
            end if not divisible by 3
    Example: "DET" "ADJ" "NN" "PRP "NN" -> "DET_ADJ_NN" "PRP_NN"
"""
def trigramify_pos_seq(pos_seq):
    trigrams = []
    for i in range(int(math.ceil(len(pos_seq)/3))):
        trigrams.append('_'.join(pos_seq[i*3:i*3+3]))
    return trigrams

if __name__=='__main__':

    #process command-line arguments for the type of review to generate, the part-of-speech generation method, 
    #and the method for selecting words for each part of speech
    word_selection_type = sys.argv[5]
    pos_type = sys.argv[4]
    review_type = sys.argv[3]

    if int(review_type) == 0:
        ngram.sentence_extraction()
        sys.exit(0)

    randomly_chosen_pos_sequences = []

    #----------------
    #populate randomly_chosen_pos_sequences with part-of-speech sequences
    if int(pos_type) == 1:
        pos_sequences = build_POS_table("./data/" + sys.argv[1] + "/pos.txt")
        while len(randomly_chosen_pos_sequences) != min(len(pos_sequences), 4):
            x = random.randint(0,len(pos_sequences) - 1)
            while len(pos_sequences[x]) == 0:
                x = random.randint(0,len(pos_sequences) - 1)

            while (pos_sequences[x] in randomly_chosen_pos_sequences) or (len(pos_sequences[x]) < 4):
                x = random.randint(0,len(pos_sequences) - 1)
                while len(pos_sequences[x]) == 0:
                    x = random.randint(0,len(pos_sequences) - 1)
            randomly_chosen_pos_sequences.append(pos_sequences[x])
    elif int(pos_type) == 0:
        randomly_chosen_pos_sequences = build_Probabilistic_POS("./data/" + sys.argv[1] + "/pos.txt", "./data/" + sys.argv[1] + "/bg_emissions.txt")
    
    #----------------

    #----------------
    #outputting sentences

    tfidf_dict = tfidf()

    if int(word_selection_type) == 1:
        for i in range(len(randomly_chosen_pos_sequences)):
            #print 'heyo' + str(len(randomly_chosen_pos_sequences[i]))
            tri_pos_seq = trigramify_pos_seq(randomly_chosen_pos_sequences[i])
            randomly_chosen_pos_sequences[i] = tri_pos_seq

        for pos in randomly_chosen_pos_sequences:
            for sent in sentence(sys.argv[1], tfidf_dict, pos):
                x = 5
                #print sent.lower()

    elif int(word_selection_type) == 0:
        for pos in randomly_chosen_pos_sequences:
            for sent in sentenceBigrams(sys.argv[1], tfidf_dict, pos):
                print sent.lower()

    #----------------