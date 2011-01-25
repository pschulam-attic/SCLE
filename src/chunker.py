'''
Created on 
Sun Jan 23 11:26:17 EST 2011
@author: pschulam
'''

import nltk, os, random
from nltk.corpus import conll2000
from nltk.tag import ClassifierBasedTagger

def refresh():
    os.remove(os.getcwd() + '/' + _pickle_file)
    os.remove(os.getcwd() + '/' + _test_sents_pickle_file)

def npchunk_features(sentence, i, history):
    '''
    Defines a set of features to be extracted for a particular
    chunk tagged word in a sentence. We have the entire sentence,
    the current word index, and the history of previous tags
    available to us. 
    '''
    word, pos = sentence[i]
    if i == 0:
        prevword, prevpos = "<START>", "<START>"
    else:
        prevword, prevpos = sentence[i-1]
    if i == len(sentence) - 1:
        nextword, nextpos = "<END>", "<END>"
    else:
        nextword, nextpos = sentence[i+1]
    return {"pos": pos,
            "word": word,
            "prevpos": prevpos,
            "nextpos": nextpos,
            "prevpos+pos": "%s+%s" % (prevpos, pos),
            "pos+nextpos": "%s+%s" % (pos, nextpos),
            "tags-since-dt": tags_since_dt(sentence, i)}

def tags_since_dt(sentence, i):
    '''
    Gathers the parts of speech between the last
    determiner and the current index.
    '''
    tags = set()
    for word, pos in sentence[:i]:
        if pos == 'DT':
            tags = set()
        else:
            tags.add(pos)
    return '+'.join(sorted(tags))

class Chunker(nltk.chunk.ChunkParserI):
    '''
    Chunker for SCLE. Only chunks NP for now.
    '''
    def __init__(self):

        train_sents = conll2000.chunked_sents('train.txt', chunk_types=['NP'])
        ctagged_sents = [[((w,t),c) for (w,t,c) in nltk.chunk.tree2conlltags(sent)] for sent in train_sents]
        test_sents = conll2000.chunked_sents('test.txt', chunk_types=['NP'])
        self._test_sents = [[((w,t), c) for (w,t,c) in nltk.chunk.tree2conlltags(sent)] for sent in test_sents]
        self._tagger = ClassifierBasedTagger(train=ctagged_sents, feature_detector=npchunk_features)

    def chunk(self, sentences):
        '''
        '''
        chunked_sents - []
        for sent in sentences:
            c_sent = self._tagger.tag(sent)
            conlltags =[(w,t,c) for ((w,t),c) in c_sent]
            chunked_sents.append(nltk.chunk.conlltags2tree(conlltags))
        return chunked_sents
   
    def evaluate(self):
        '''
        Evaluate the chunker.
        '''
        print self._tagger.evaluate(self._test_sents)

