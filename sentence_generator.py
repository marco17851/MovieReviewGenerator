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
import math

#Metadata of your program
___author__ = 'Sravana Reddy'
__date__ = 'Sep 2014'
__version__ = '1'
tolerance = 3
posEmissions = defaultdict(list)
bgPosEmissions = defaultdict(list)
uniPosEmissions = defaultdict(list)
tfidf_pos_tags = ['NNP', 'VBZ', 'JJ', 'NN', 'VB', 'NNS', 'VBD', 'NNPS', 'VBG']

class TF_IDF:
    def __init__(self, docCounts):
        self.documentCounts = docCounts

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

#returns a list of part-of-speech sequences, each corresponding to a sentence in posFile
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
            total_sequence.append(tags[1])
    return posTable

def get_document_counts(rootdir, documentCounts):
    numberDocuments = 0
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            #f = file.read()
            fileCount = defaultdict(int)
            pathName = os.path.join(subdir, file)
            if pathName.endswith('summaries.txt') or pathName.endswith('texts.txt'):
                if pathName.endswith('summaries.txt'):
                    alpha = 0.5 # constant for summaries
                else:
                    alpha = 1
                numberDocuments += 1
                f = open(pathName).read()
                for word in f.split():
                    fileCount[word] += 1
                for word in fileCount:
                    documentCounts[word] += 1*alpha                
    return numberDocuments

def tfidf_counts():  
    documentCounts = defaultdict(int)
    numberDocs = get_document_counts("./data", documentCounts)
    for word, count in documentCounts.iteritems():
        documentCounts[word] = str(math.log(numberDocs/count))
    return documentCounts

def tfidf():
    tfidf_dict = defaultdict(float)
    for line in open('./tfidf.txt'):
        words = line.split('|')
        try:
            tfidf_dict[words[0]] = float(words[1].strip())
        except:
            continue
    return tfidf_dict

class WordFreq:
    def __init__(self, w, f):
        self.word = w
        self.freq = f

    def __repr__(self):
        return '(' + self.word + ' ' + str(self.freq) + ')'

#returns a sentenceID dictionary {word -> id's of sentences the word appears in}
def create_sentence_id_dict(productID):
    id_dict = defaultdict(list)
    for line in open('./data/' + productID + '/sentence_ids.txt'):
        tuples = line.split(':')
        if len(tuples) != 2:
            continue
        word = tuples[0].translate(string.maketrans("",""), string.punctuation).lower()
        for num in tuples[1].split():
            id_dict[word].append(int(num))
    return id_dict

#creates {part-of-speech sequence -> words} dictionary based on the emissions file
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

#returns dictionary {word -> {pos -> [words corresponding to pos]}}
def pos_to_words(productID):
    arpa_dict = defaultdict(lambda: defaultdict(list))
    curr_key = ''
    for line in open('./data/' + productID + '/reviews.arpa'):
        words = line.split('|')
        if len(words) == 1:
            curr_key = words[0].strip()
            continue
        for w in words[1].split():
            arpa_dict[curr_key][words[0].strip()].append(w.strip())
    #print arpa_dict['<s>']
    return arpa_dict

def getWordFromUnigramEmissions(ID, pos):
    array = []
    found = 0

    file = open("./data/" + ID + "/emissions.txt")
    for line in file:
        words = line.strip().split("\t")
        if words[0] == pos:
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

    #print array
    rand = 0
    try:
        rand = random.randint(0, len(array)-1)
    except:
        if len(array) == 0:
            return "..."
    return array[rand]

#returns list of sentences corresponding to pos_sequence
def sentenceBigrams(productID, tfidf_counts, pos_sequence):

    sentences = []
    arpa_dict = pos_to_words(productID)
    #print arpa_dict['<s>']['PRP']
    #print pos_sequence
    for i in range(1):
        sentence = ''
        curr_key = '<s>'
        pos_seq_feasible = True
        for pos in pos_sequence:
            words = arpa_dict[curr_key][pos]
            #print curr_key + '|' + pos + '|' + str(words)
            if len(words) == 0:
                #pos_seq_feasible = False
                #break
                selected_word = getWordFromUnigramEmissions(productID, pos)
                curr_key = selected_word
                sentence += selected_word + ' '
            else:
                x = random.randint(0,len(words) - 1)
                #print words[x]
                #print '------'
                sentence += words[x] + ' '
                curr_key = words[x]
        if pos_seq_feasible == True:
            sentences.append(sentence)
    #print len(sentences)
    sent_scores = []
    #print tfidf_counts
    #print '--------------'
    for sent in sentences:
        tfidf_score = 0
        sent_words = sent.split()
        for i in range(len(pos_sequence)):

            if pos_sequence[i] in tfidf_pos_tags:
                #print 'word: ' + sent_words[i]
                #print 'tfidf_score: ' + tfidf_counts[sent_words[i]]
                tfidf_score += float(tfidf_counts[sent_words[i]])
        sent_scores.append(SentScore(sent, tfidf_score))
    sent_scores.sort(reverse=True)

    best_sentences = []
    for i in range(min( len(sent_scores), 1)):
        best_sentences.append(sent_scores[i].sentence)
    return best_sentences


#returns array of sentences that adhere to pos_sequence (a part of speech tag sequence)
def sentence(productID, tfidf_counts, pos_sequence):

    sentence_id_dict = create_sentence_id_dict(productID)

    populateDicts('/tr_emissions.txt', productID, posEmissions)
    populateDicts('/bg_emissions.txt',productID, bgPosEmissions)
    populateDicts('/emissions.txt',productID, uniPosEmissions)        

    sentences = []
    for i in range(10):
        computed_sent = generateSentence(pos_sequence, posEmissions, sentence_id_dict)
        if computed_sent == None:
            return None
        sentences.append(computed_sent)

    sent_scores = []
    #print tfidf_counts
    #print '--------------'
    for sent in sentences:
        tfidf_score = 0
        sent_words = sent.split()
        separated_pos_seq = separate_pos(pos_sequence)
        for i in range(len(separated_pos_seq)):
            if separated_pos_seq[i] in tfidf_pos_tags:
                #print 'word: ' + sent_words[i]
                #print 'tfidf_score: ' + str(tfidf_counts[sent_words[i]])
                tfidf_score += float(tfidf_counts[sent_words[i]])
        sent_scores.append(SentScore(sent, tfidf_score))
    sent_scores.sort(reverse=True)

    best_sentences = []
    for i in range(min( len(sent_scores), 1)):
        best_sentences.append(sent_scores[i].sentence)
    return best_sentences

def separate_pos(pos_sequence):
    pos_seq = []
    for pos in pos_sequence:
        for p in pos.split('_'):
            pos_seq.append(p)

    return pos_seq

def overlap(pos_sequence):
    #print pos_sequence
    overlapping_pos_seq = []

    unigram_pos_seq = []
    for pos in pos_sequence:
        for p in pos.split('_'):
            unigram_pos_seq.append(p)

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


#generates a single sentence based on part of speech sequence (pos_sequence), emission probabilities (posEmissions), and sentence_ids (id_dictionary)
def generateSentence(pos_sequence, posEmissions, id_dictionary):
    sentence = ""
    #print posEmissions
    #print pos_sequence
    #print overlap(pos_sequence)
    #print '------'
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
                    #sentence += word + ' '
                    wordsToAdd.append(word)

            if len(pos.split('_')) == 1:
                for word in uniPosEmissions[pos][0].word.split('_'):
                    wordsToAdd.append(word)
                    #sentence += word + ' '
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
    
    #print len(sentence.split())
    #print '-------'
    return sentence

#generates a single sentence based on part of speech sequence (pos_sequence), emission probabilities (posEmissions), and sentence_ids (id_dictionary)
#the sentence ids restricts the words in the output sentence to come from nearby sentences in the reviews
def generateSentenceOld(pos_sequence, posEmissions, id_dictionary):
    
    sentence = ""
    
    for pos in pos_sequence:
        #try 19 times to find a sentence matching the constraints
        #if unsuccessful, generate a sentence that just adheres the pos_sequence, and ignore sentence id restriction
        for i in range(20):
            stop_checking_id_restriction = False
            if i == 19:
                stop_checking_id_restriction = True

            prev_word_sentence_ids = [-1]
            success = False
            #generate a random number between 0 and 1, representing which trigram to select
            rand_num = random.random()
            
            if pos not in posEmissions:
                return None

            rand_num -= posEmissions[pos][0].freq
            for i in range(1, len(posEmissions[pos])):
                if rand_num > 0:
                    rand_num -= posEmissions[pos][i].freq
                else:
                    #words is the randomly chosen trigram
                    words = posEmissions[pos][i].word.split("_")
                    
                    #check that the chosen trigram is close to the previous trigram in the output sentence
                    #based on whether the sentence id's of the currently chosen trigram and previous trigram are close values
                    prev_word_sentence_ids = within_tolerance(prev_word_sentence_ids, words, id_dictionary)
                    
                    #if the sentence id's of the previous and current trigram are not close, break, and try again
                    if len(prev_word_sentence_ids) == 0 and not stop_checking_id_restriction:
                        break
                    
                    #success = True means we have found a trigram whos sentence id is close to the previously chosen trigram
                    # and therefore adheres to the sentence id restriction
                    success = True

                    #add the trigram to the sentence
                    if words[0] == "<s>":
                        for y in range(1, len(words)):
                            sentence += words[y] + ' '
                    else:
                        for y in range(0, len(words)):
                            sentence += words[y] + ' '
                    break
            #if success is False, we need to keep generating trigrams for a total of 20 times until the sentence id constraint is met
            #otherwise, break, and proceed with the next part of speech sequence
            if success == True:
                break

    return sentence

#id_dictionary has the sentence id's for each word
#words is the current trigram
#prev_word_sentence_id holds the sentence id's of the previous trigram

#if prev_word_sentence_id has sentence id of -1, then there was no previous trigram, so return the sentence_ids of the current trigram 
#otherwise, check if sentence id's of prev_word_sentence_id is within 3 (specified in tolerance global variable) of the sentence_id's of the current trigram,
#and return the sentence id's of the current trigram that satisfy the constraint
def within_tolerance(prev_word_sentence_id, words, id_dictionary):
    
    #common_ids holds the sentence_id's of each word in the current trigram
    common_ids = []
    for w in words:
        if w == '<s>':
            continue
        else:
            common_ids.append(id_dictionary[w.lower()])

    #trigram_ids is the intersection of the sentence_id's of each word in the current trigram
    #the code below finds the intersection
    trigram_ids = []
    for id in common_ids[0]:
        for i in range(1,len(common_ids)):
            match = False
            for other_id in common_ids[i]:
                if math.fabs(id - other_id) <= tolerance:
                    match = True
            if match == False:
                break
            if i == len(common_ids) - 1:
                trigram_ids.append(id)

    if prev_word_sentence_id[0] == -1:
        return trigram_ids

    #find the sentence_ids between the previous trigram's sentence ids and the current trigram's sentence ids
    within_range_sentence_ids = []
    for id in trigram_ids:
        for other_id in prev_word_sentence_id:
            if math.fabs(other_id - id) <= tolerance:
                within_range_sentence_ids.append(id)
    return within_range_sentence_ids

#groups a part of speech sequence into triples: ['DET', 'ADJ', 'NOUN', 'PREP', 'DET', 'NOUN'] -> [ ['DET', 'ADJ', 'NOUN'], ['PREP', 'DET', 'NOUN'] ]
def trigramify_pos_seq(pos_seq):
    trigrams = []
    for i in range(int(math.ceil(len(pos_seq)/3))):
        trigrams.append('_'.join(pos_seq[i*3:i*3+3]))
    return trigrams

if __name__=='__main__':

    trigram_level = 2
    bigram_level = 3

    #----------------
    #populate randomly_chosen_pos_sequences with part-of-speech sequences

    pos_sequences = build_POS_table("./data/" + sys.argv[1] + "/pos.txt")
    randomly_chosen_pos_sequences = []
    while len(randomly_chosen_pos_sequences) != min(len(pos_sequences), 4):
        x = random.randint(0,len(pos_sequences) - 1)
        while len(pos_sequences[x]) == 0:
            x = random.randint(0,len(pos_sequences) - 1)

        while (pos_sequences[x] in randomly_chosen_pos_sequences) or (len(pos_sequences[x]) < 4):
            x = random.randint(0,len(pos_sequences) - 1)
            while len(pos_sequences[x]) == 0:
                x = random.randint(0,len(pos_sequences) - 1)
        randomly_chosen_pos_sequences.append(pos_sequences[x])

    #----------------

    #----------------
    #outputting sentences

    tfidf_dict = tfidf()

    if int(sys.argv[2]) == trigram_level:
        for i in range(len(randomly_chosen_pos_sequences)):
            #print 'heyo' + str(len(randomly_chosen_pos_sequences[i]))
            tri_pos_seq = trigramify_pos_seq(randomly_chosen_pos_sequences[i])
            randomly_chosen_pos_sequences[i] = tri_pos_seq

        for pos in randomly_chosen_pos_sequences:
            for sent in sentence(sys.argv[1], tfidf_dict, pos):
                print sent.lower()

    elif int(sys.argv[2]) == bigram_level:
        for pos in randomly_chosen_pos_sequences:
            for sent in sentenceBigrams(sys.argv[1], tfidf_dict, pos):
                print sent.lower()
                sys.exit()


