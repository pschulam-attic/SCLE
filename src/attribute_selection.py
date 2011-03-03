'''
Created on Feb 19, 2011

@author: pschulam
'''

from webcorpus import WebCorpus
from string import lower

# Attributes taken from Hartung and Frank
attributes = [
              'color',
              'direction',
              'duration',
              'shape',
              'size',
              'smell',
              'speed',
              'taste',
              'temperature',
              'weight'
              ]

JJ_jj_attr_patterns = [
                    #"\"%s or %s %s\"",          # JJ or JJ ATTR
                    "\"is %s in %s\"",          # is JJ in ATTR
                    "\"was %s in %s\"",         # was JJ in ATTR
                    "\"are %s in %s\"",         # are JJ in ATTR
                    "\"were %s in %s\"",        # were JJ in ATTR
                    "\"is %s of %s\"",          # is JJ of ATTR
                    "\"was %s of %s\"",         # was JJ of ATTR
                    "\"are %s of %s\"",         # are JJ of ATTR
                    "\"were %s of %s\""         # were JJ of ATTR
                    ]

JJ_attr_nn_jj_patterns = [
                    "\"%s of * %s is %s\"",     # ATTR of DT? NN is JJ
                    "\"%s of * %s was %s\"",    # ATTR of DT? NN was JJ
                    ]

JJ_nn_attr_jj_patterns = [
                       "\"%s's %s is %s\"",        # NN's ATTR is JJ
                       "\"%s's %s was %s\"",       # NN's ATTR was JJ
                       ]

NN_nn_jj_attr_patterns = [
                    "\"%s with * %s %s\"",         # NN with DT? RB? JJ ATTR
                    "\"%s without * %s %s\"",       # NN without DT? RB? JJ ATTR
                    "\"The %s's * %s %s\"",         # DT NN's RB? JJ ATTR
                    "\"%s has a * %s %s\"",         # NN has a RB? JJ ATTR
                    "\"%s has an * %s %s\"",        # NN has an RB? JJ ATTR
                    "\"%s had a * %s %s\"",         # NN had a RB? JJ ATTR
                    "\"%s had an * %s %s\""        # NN had an RB? JJ ATTR
                    ]

NN_attr_jj_nn_patterns = [
                          "\"the %s of * %s %s\""   # The ATTR of DT? RB? JJ NN
                          ]

def select_attribute(NN, JJ):
    NN = lower(NN)
    JJ = lower(JJ)
    search = WebCorpus()
    
    # Get counts for the attribute dimensions for both the noun and adjective
    nn_vector = dict([(att, 0) for att in attributes])
    jj_vector = dict([(att, 0) for att in attributes])
    for ATTR in attributes:
        # Collect noun numbers
        for p in NN_nn_jj_attr_patterns:
            results = search.get_results(p % (NN, JJ, ATTR))
            nn_vector[ATTR] += search.get_count(results)
        for p in NN_attr_jj_nn_patterns:
            results = search.get_results(p % (ATTR, JJ, NN))
            nn_vector[ATTR] += search.get_count(results)
            
        # Collect adjective numbers
        for p in JJ_jj_attr_patterns:
            results = search.get_results(p % (JJ, ATTR))
            jj_vector[ATTR] += search.get_count(results)
        for p in JJ_attr_nn_jj_patterns:
            results = search.get_results(p % (ATTR, NN, JJ))
            jj_vector[ATTR] += search.get_count(results)
        for p in JJ_nn_attr_jj_patterns:
            results = search.get_results(p % (NN, ATTR, JJ))
            jj_vector[ATTR] += search.get_count(results)
    sel_vector = {}
    for k,v in nn_vector.items():
        sel_vector[k] = v * jj_vector[k]
    attribute = ""
    max = 0
    for k,v in sel_vector.items():
        if v > max:
            attribute = k
    return attribute