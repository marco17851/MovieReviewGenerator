from __future__ import division          #integer division
from collections import defaultdict
import os
import random
import string        #some string-related utilities
import sys        #for command-line args
import re    #for regular expressions
import math

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

def parse_essayfile(filename):
    essay = open(filename.strip())
    array = []
    for line in essay:
        new = line.lower().strip().split(".")
        for x in new:
            if x == "" or x == " ":
                continue
            else:
                array.append([x])
    return array
    #return map(lambda sentence: sentence.lower().split(),
    #           open(filename.strip()).readlines())

def write_results(hypotheses):
    """hypotheses is a dictionary mapping essays (denoted by their filenames) to languages"""
    o = open('results.txt', 'w')
    for essay in hypotheses:
        o.write(essay+','+hypotheses[essay]+'\n')
    o.close()

def sentence_grams(essay):    
    array = []
    for sentence in essay:
        array.append([sentence])

    return array
        
if __name__=='__main__':

    #n-gram model parameters (to fiddle with)
    order = 3
    lambdaweight = 0.7
    unkcount = 0.5
    
    #reads training and test data from the nli folder (relative path).
    #creates a "training" dictionary which maps each language to a list of the associated essay files
    training = defaultdict(list)
    traininginfo = open('./nli/training_langid.txt', 'r')
    for line in traininginfo:
        essayfile, language = line.strip().split(',')
        training[language].append(essayfile)

    #store a "testing" essay list.
    testing = open('./nli/testing_list.txt', 'r')

    #train a language model for every language in the training set
    """
    models = {}
    for language in training:
        models[language] = NGramModel(order, unkcount, lambdaweight)
        
        for essayfile in training[language]:
            essay = parse_essayfile('./nli/training/' + essayfile)
            models[language].count_from_training(essay)
        
        models[language].normalize()
        print "Trained a model on", language
    """
    
    models = {}
    models["summaries"] = NGramModel(order, unkcount, lambdaweight)
    models["summaries"].count_from_training(parse_essayfile("summaries.txt"))
    models["summaries"].normalize()
    
    #models are all trained, now test
    #essay = parse_essayfile('./nli/testing/88.txt')
    essay = parse_essayfile("summaries.txt")
    components = sentence_grams(essay)
    print components

    perplexities = map(lambda (language, model): (language, model.compute_perplexity(essay)),
                           models.items())
    print perplexities
    """
    hypotheses = {}
    for essayfile in testing:
        essay = parse_essayfile(os.path.join('nli', 'testing', essayfile))
        
        perplexities = map(lambda (language, model): (language, model.compute_perplexity(essay)),
                           models.items())   #compute the perplexity of each language model on this essay

        #print perplexities
        hypotheses[essayfile] = min(perplexities,
                                    key=lambda x:x[1])[0]
    
    write_results(hypotheses)
    """
    print "Testing completed"