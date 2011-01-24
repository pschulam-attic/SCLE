'''
Created on 
Sun Jan 23 11:26:17 EST 2011
@author: pschulam
'''

import nltk
from nltk.corpus import conll2000

def npchunk_features(sentence, i, history):
    '''
    Defines a set of features to be extracted for a particular
    chunk tagged word in a sentence. We have the entire sentence,
    the current word index, and the history of previous tags
    available to us. For now we will only use the POS of the current
    word as a feature, but we can add more later.
    '''
    word, pos = sentence[i]
    return {"pos": pos}

class ChunkTagger(nltk.TaggerI):
    '''
    Assigns chunk tags to each word given its POS tag.
    Uses a maximum entropy classifier that is trained on a set of
    sentences that have been both POS and chunk tagged.
    '''

    def __init__(self, train_sents):
        '''
        Constructor. Must pass a set of sentences that have been
        both POS and chunk tagged for training.
        '''
        train_set = []
        for ctagged_sent in train_sents:
            pos_tagged_sent = nltk.tag.untag(ctagged_sent)
            history = []
            for i, (word, ctag) in enumerate(ctagged_sent):
                featureset = npchunk_features(pos_tagged_sent, i, history)
                train_set.append( (featureset, ctag) )
                history.append(ctag)
            self.classifier = nltk.MaxentClassifier.train(
                    train_set, algorithm='megam', trace=0)

    def tag(self, sentence):
        '''
        Given a POS tagged sentence, produces the most probable
        chunk tag using a maximum entropy classifier.
        '''
        history = []
        for i, word in enumerate(sentence):
            featureset = npchunk_features(sentence, i, history)
            tag = self.classifier.classify(featureset)
            history.append(tag)
        return zip(sentence, history)

class Chunker(nltk.ChunkParserI):
    '''
    Chunker for SCLE. Only chunks NP for now.
    '''
    def __init__(self):
        train_sents = conll2000.chunked_sents('train.txt', chunk_types=['NP'])
        ctagged_sents = [[((w,t),c) for (w,t,c) in nltk.chunk.tree2conlltags(sent)] for sent in train_sents]
        self.tagger = ChunkTagger(ctagged_sents)

    def parse(self, sentence):
        '''
        Accepts a sentence with POS tags and produces a NP chunk parse.
        '''
        ctagged_sents = self.tagger.tag(sentence)
        conlltags = [(w,t,c) for ((w,t),c) in ctagged_sents]
        return nltk.chunk.conlltags2tree(conlltags)

