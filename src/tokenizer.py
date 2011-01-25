'''
Created on Jan 20, 2011

@author: pschulam
'''

from nltk import sent_tokenize, word_tokenize

class Tokenizer(object):
    '''
    Does all of the steps necessary before tagging and chunking.
    Mainly tokenizes.
    '''

    def __init__(self):
        '''
        Constructor. Doesn't do anything.
        '''
        pass

    def tokenize(self, filename):
        '''
        Split the text in the given file into a list of lists of words.
        Each nested list should be one sentence in the document.
        '''
        fd = open(filename, 'r')
        doc = fd.read()
        fd.close()
        sents = sent_tokenize(doc)
        sents = [word_tokenize(sent) for sent in sents]
        return sents

