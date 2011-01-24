'''
Created on Jan 20, 2011

@author: pschulam
'''

from nltk.tag import DefaultTagger, UnigramTagger, BigramTagger, TrigramTagger, brill
from nltk.corpus import brown
from cPickle import dump, load
import os

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

        self._pickle_file = 'tagger.pkl'

        # Before building a new tagger check if one has already been pickled
        if (os.path.exists(os.getcwd() + '/' + self._pickle_file)):
            input = open(self._pickle_file, 'rb')
            self._tagger = load(input)
            input.close()
            
        # Primitives necessary for training the Brill tagger.
        # Taken from cookbook
        else:
            brown_tagged_sents = brown.tagged_sents()
            default_tagger = DefaultTagger('NN')
            tagger_classes = [UnigramTagger, BigramTagger, TrigramTagger]
            initial_tagger = backoff_tagger(brown_tagged_sents, tagger_classes, backoff=default_tagger)
            sym_bounds = [(1,1), (2,2), (1,2), (1,3)]
            asym_bounds = [(-1, -1), (1,1)]
            templates = [
                brill.SymmetricProximateTokensTemplate(brill.ProximateTagsRule, *sym_bounds),
                brill.SymmetricProximateTokensTemplate(brill.ProximateWordsRule, *sym_bounds),
                brill.ProximateTokensTemplate(brill.ProximateTagsRule, *asym_bounds),
                brill.ProximateTokensTemplate(brill.ProximateWordsRule, *asym_bounds)]

            # Train the tagger
            trainer = brill.FastBrillTaggerTrainer(initial_tagger, templates, deterministic=True)
            self._tagger = trainer.train(brown_tagged_sents)

            #Pickle the trained tagger
            output = open(self._pickle_file, 'wb')
            dump(self._tagger, output, -1)
            output.close()

    def _refresh(self):
        '''
        Removes the pickle file containing the tagger.
        '''
        os.remove(os.getcwd() + '/' + self._pickle_file)

    def _evaluate(self):
        '''
        Evaluate the tagger
        '''
        pass
        
    def tag(self, tokens):
        '''
        Tags the tokens provided. Returns a list of tuples containing each word
        and its tag. The tokens must be provided as a list of sentences, where each sentence is a
        list of word tokens.
        '''
        tags = []
        
        for sent in tokens:
            tags.append(self._tagger.tag(sent))
            
        return tags
