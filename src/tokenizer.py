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

    def __init__(self, filename):
        '''
        Constructor
        
        Takes the document that will be processed as input
        '''
        fd = open(filename, 'r')
        doc = fd.read()
        fd.close()
        self._sentences = sent_tokenize(doc)
        self._sentences = [word_tokenize(sent) for sent in self._sentences]

    def get_sentences(self):
        '''
        Returns the sentences stored in this instance
        '''
        return self._sentences
        
    def print_sentences(self):
        '''
        Prints out the the document.
        '''
        for sent in self._sentences:
            for word in sent:
                print word,
            print
