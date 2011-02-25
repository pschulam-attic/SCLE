'''
Created on Feb 19, 2011

@author: pschulam
'''

from Google import search
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
                    "\"%s or %s %s\"",          # JJ or JJ ATTR
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
    # Get counts for the attribute dimensions for both the noun and adjective
    nn_vector = dict([(att, 0) for att in attributes])
    jj_vector = dict([(att, 0) for att in attributes])
    for ATTR in attributes:
        # Collect noun numbers
        for p in NN_nn_jj_attr_patterns:
            print "searching " + p % (NN, JJ, ATTR)
            num_results = search(p % (NN, JJ, ATTR), 1000)
            nn_vector[ATTR] += num_results
        for p in NN_attr_jj_nn_patterns:
            num_results = search(p % (ATTR, JJ, NN), 1000)
            nn_vector[ATTR] += num_results
        # Collect adjective numbers
        for p in JJ_jj_attr_patterns:
            num_results = search(p % (JJ, ATTR), 1000)
            jj_vector[ATTR] += num_results
        for p in JJ_attr_nn_jj_patterns:
            num_results = search(p % (ATTR, NN, JJ), 1000)
            jj_vector[ATTR] += num_results
        for p in JJ_nn_attr_jj_patterns:
            num_results = search(p % (NN, ATTR, JJ), 1000)
            jj_vector[ATTR] += num_results
    sel_vector = {}
    for k,v in nn_vector:
        sel_vector[k] = v * jj_vector[k]
    attribute = ""
    max = 0
    for k,v in sel_vector:
        if v > max:
            attribute = k
    return attribute