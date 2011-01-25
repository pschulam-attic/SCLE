'''
Created on Jan 20, 2011

@author: pschulam
'''

from nltk.tag import DefaultTagger, UnigramTagger, BigramTagger, TrigramTagger, brill
from nltk.corpus import brown
from cPickle import dump, load
import os, random

_pickle_file = 'pickles/tagger.pkl'
_test_sents_pickle_file = 'pickles/tagger_test_sents.pkl'

def refresh():
    '''
    Remove the pickle files for the tagger and test sentences.
    '''
    os.remove(os.getcwd() + '/' + _pickle_file)
    os.remove(os.getcwd() + '/' + _test_sents_pickle_file)

def backoff_tagger(train_sents, tagger_classes, backoff=None):
    '''
    Creates a backoff tagger given the training sentences and
    the sequence of taggers specified in tagger_classes.
    '''
    for cls in tagger_classes:
        backoff = cls(train_sents, backoff=backoff)
    return backoff

class Tagger(object):
    '''
    The tagger tags the text that has been preprocessed.
    The current implementation will use a Brill tagger, but we will
    test other taggers to check accuracy with respect to NPs and
    VPs containing adjective predicates.
    '''

    def __init__(self):
        '''
        Constructor
        '''

        # Before building a new tagger check if one has already been pickled
        if (os.path.exists(os.getcwd() + '/' + _pickle_file)):
            input = open(_pickle_file, 'rb')
            self._tagger = load(input)
            input.close()
            input = open(_test_sents_pickle_file, 'rb')
            self._test_sents = load(input)
            input.close()
            
        # Primitives necessary for training the Brill tagger.
        # Taken from cookbook
        else:
            tagged_sents = list(brown.tagged_sents())
            random.shuffle(tagged_sents)
            split_index = int(round(0.8 * len(tagged_sents)))
            train_sents = tagged_sents[:split_index]
            self._test_sents = tagged_sents[split_index:]
            default_tagger = DefaultTagger('NN')
            tagger_classes = [UnigramTagger, BigramTagger, TrigramTagger]
            initial_tagger = backoff_tagger(train_sents, tagger_classes, backoff=default_tagger)
            sym_bounds = [(1,1), (2,2), (1,2), (1,3)]
            asym_bounds = [(-1, -1), (1,1)]
            templates = [
                brill.SymmetricProximateTokensTemplate(brill.ProximateTagsRule, *sym_bounds),
                brill.SymmetricProximateTokensTemplate(brill.ProximateWordsRule, *sym_bounds),
                brill.ProximateTokensTemplate(brill.ProximateTagsRule, *asym_bounds),
                brill.ProximateTokensTemplate(brill.ProximateWordsRule, *asym_bounds)]

            # Train the tagger
            trainer = brill.FastBrillTaggerTrainer(initial_tagger, templates, deterministic=True)
            self._tagger = trainer.train(train_sents)

            #Pickle the trained tagger
            if not os.path.exists(os.getcwd() + '/pickles/'):
                os.mkdir(os.getcwd() + '/pickles/')
            output = open(_pickle_file, 'wb')
            dump(self._tagger, output, -1)
            output.close()
            output = open(_test_sents_pickle_file, 'wb')
            dump(self._test_sents, output, -1)
            output.close()

    def evaluate(self):
        '''
        Evaluate the tagger
        '''
        print self._tagger.evaluate(self._test_sents)
        
    def tag(self, sentences):
        '''
        Tags the tokens provided. Returns a list of tuples containing each word
        and its tag. The tokens must be provided as a list of sentences, where each sentence is a
        list of word tokens.
        '''
        tagged_sents = []
        
        for sent in sentences:
            tagged_sents.append(self._tagger.tag(sent))
            
        return tagged_sents
