'''
Created on Jan 20, 2011

@author: pschulam
'''

from nltk import sent_tokenize, word_tokenize

class Preprocessor(object):
    '''
    Does all of the steps necessary before tagging and chunking.
    '''

    def __init__(self, document):
        '''
        Constructor
        
        Takes the document that will be processed as input
        '''
        self._sentences = sent_tokenize(document)
        self._sentences = [word_tokenize(sent) for sent in self._sentences]

    def get_sentences(self):
        '''
        Prints the sentences stored in this instance
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
