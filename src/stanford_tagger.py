'''
Created on Feb 17, 2011

@author: pschulam
'''

from os import system
from string import split

path = "/Users/pschulam/Desktop/Thesis/src/stanford-postagger/"
memory = "-mx600m"
classpath = "-classpath %sstanford-postagger.jar" % path
tagger = "edu.stanford.nlp.tagger.maxent.MaxentTagger"
model = "-model %smodels/bidirectional-distsim-wsj-0-18.tagger" % path

def tag(filename):
    output = filename[:-3] + 'tagged'
    system("java %s %s %s %s -textFile %s > %s" % (memory, classpath, tagger, model, filename, output))
    stanford2collins(output)
    return output

def stanford2collins(filename):
    input = open(filename, 'r')
    sentences = []
    for line in input:
        tokens = split(line)
        tokens = [tuple(split(t, '_')) for t in tokens]
        sentences.append(tokens)
    input.close
    str_sentences = []
    for s in sentences:
        str_sent = "%s " % len(s)
        for word in s:
            str_sent += "%s %s " % word
        str_sentences.append(str_sent)
    output = open(filename, 'w')
    for s in str_sentences:
        output.write("%s\n" % s)
    output.close
    
    
    
    