from __future__ import division          #integer division
from collections import defaultdict
import random
import string        #some string-related utilities
import sys        #for command-line args
import re    #for regular expressions
import math
import misc_func
#Program is adapted from Prof. Reddy's Assignment 2 solution.

tfidf_pos_tags = ['NNP', 'VBZ', 'JJ', 'NN', 'VB', 'NNS', 'VBD', 'NNPS', 'VBG']

class NGramModel:
    def __init__(self, order, unkcount, lambdaweight):
        self.order = order
        self.freqs = []   #relative frequencies of n-grams of order 0 to n-1
        for order in range(self.order+1):
            self.freqs.append(defaultdict(lambda : defaultdict(float)))
            
        self.lambdaweight = lambdaweight   #for linear interpolation

        self.unkcount = unkcount
        
    def count_from_training(self, text):
        """read in a text as a list of sentences, aggregate n-gram counts for order 0 to n-1"""
        for sentence in text:
            for wi, word in enumerate(sentence):
                context = tuple(['<s>']*(self.order-wi)+sentence[max(wi-self.order, 0):wi])  #context padded with <s> tags if necessary
                for contextstart in range(len(context)+1):   #counts for order n-1 and all orders until 0
                    self.freqs[len(context)-contextstart][context[contextstart:]][word]+=1
                    
            #model the </s> tag too
            wi = len(sentence)
            context = tuple(['<s>']*(self.order-wi)+sentence[max(wi-self.order, 0):wi])
            for contextstart in range(len(context)):
                self.freqs[len(context)-contextstart][context[contextstart:]]['</s>']+=1
                

    def normalize(self):
        """normalize all counts to relative frequencies"""

        #first assign a count for unseen words
        self.freqs[0][()]['<UNK>'] = self.unkcount
        
        for order in range(self.order+1):
            for context in self.freqs[order]:
                total = sum(self.freqs[order][context].values())
                for word in self.freqs[order][context]:
                    self.freqs[order][context][word]/=total

            
    def compute_int_probability(self, word, maxcontext):
        """compute probability with linear interpolation"""
        if maxcontext == ():  #unigram context
            if word in self.freqs[0][()] and self.freqs[0][()][word]>0:  #defaultdict behavior makes this necessary
                return self.freqs[0][()][word]
            return self.freqs[0][()]['<UNK>']

        return self.lambdaweight*self.freqs[len(maxcontext)][maxcontext][word] + \
            (1-self.lambdaweight)*self.compute_int_probability(word, maxcontext[1:])

    def compute_perplexity(self, testessay):
        """computes the perplexity of this model on an essay"""
        cross_ent = 0.0
        numtokens = 0
        for sentence in testessay:
            for wi, word in enumerate(sentence):
                context = tuple(['<s>']*(self.order-wi)+sentence[max(wi-self.order, 0):wi])
                cross_ent -= math.log(self.compute_int_probability(word, context), 2)
                numtokens+=1
                
            #prob of '</s>' tag
            wi = len(sentence)
            context = tuple(['<s>']*(self.order-wi)+sentence[max(wi-self.order, 0):wi])
            cross_ent -= math.log(self.compute_int_probability(word, context), 2)
            numtokens+=1
        return 2**(cross_ent/numtokens)

class SentenceScore:
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

def parse_essayfile(filename):
    essay = open(filename.strip())
    array = []
    for line in essay:
        new = line.lower().strip().split(".")
        for x in new:
            if x == "" or x == " " or len(x) < 20:
                continue
            else:
                #print x.split()
                array.append(x.split())
    return array

def sentence_grams(essay):
    array = []

    for index, sentence in enumerate(essay):
        array.append([sentence])

    return array


def tfidf():
    tfidf_dict = defaultdict(float)
    for line in open('./tfidf.txt'):
        words = line.split('|')
        try:
            tfidf_dict[words[0]] = float(words[1].strip())
        except:
            continue
    return tfidf_dict

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

if __name__=='__main__':

    #n-gram model parameters
    order = 3
    lambdaweight = 0.7
    unkcount = 0.5

    #train a language model on the summaries of all movie reviews
    models = {}
    models['summaries'] = NGramModel(order, unkcount, lambdaweight)
    models['summaries'].count_from_training(parse_essayfile('./allsummaries.txt'))

    models['summaries'].normalize()

    #essay is an array of sentences, where each sentence is an array of words
    #as an example: essay = [["that's", 'original,', 'but', 'not', 'independent'], ['<br', '/><br', '/>the', 'film', 'is', 'never', 'scary']]
    essay = parse_essayfile('./data/' + sys.argv[1] + '/texts.txt')

    #the compute_perplexity method takes an array of sentences, and calculates its perplexity
    #we want to compute the perplexity of each summary sentence, so we construct an array containing a single summary sentence
    #so we can legally pass that array to compute_perplexity

    #components is an array of array of sentences, where each inner array corresponds to a single summary sentence
    components = sentence_grams(essay)

    sent_scores = []

    for c in components:

        #compute the perplexity of c, which is an array containing a single summary sentence
        perplexities = map(lambda (language, model): (language, model.compute_perplexity(c)),
                           models.items())

        #debugging:
        #print c
        #print perplexities
        #print perplexities[0][1]

        #make a SentenceScore object that contains the summary sentence and its perplexity
        sent_scores.append(SentenceScore(' '.join(c[0]), perplexities[0][1]))

    #sort sentences by perplexity
    sent_scores.sort()

    #keep the top 1/5th sentences with the lowest perplexities
    sentences = sent_scores[1:int(len(sent_scores)/5)]

    tfidf_dict = tfidf()

    #to score each sentence, compute the TFIDF scores of each word in the sentence, sum up the scores, and divide by the number of words
    #output the sentences with the highest scores
    
    for sent in sentences:
        tfidf_score = 0.0
        sent_words = sent.sentence.split()
        for w in sent_words:
            tfidf_score += float(tfidf_dict[w])

        tfidf_score /= len(sent_words)
        sent_scores.append(SentScore(sent, tfidf_score))
    sent_scores.sort(reverse=True)

    best_sentences = []
    for i in range(min( len(sent_scores), 10)):
        print sent_scores[i].sentence

