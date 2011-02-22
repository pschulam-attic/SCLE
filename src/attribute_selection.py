'''
Created on Feb 19, 2011

@author: pschulam
'''

from Google import Google, search

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

jj_attr_patterns = [
                    "%s of * %s is %s",     # ATTR of DT? NN is JJ
                    "%s of * %s was %s",    # ATTR of DT? NN was JJ
                    "%s or %s %s",          # JJ or JJ ATTR
                    "%s's %s is %s",        # NN's ATTR is JJ
                    "%s's %s was %s",       # NN's ATTR was JJ
                    "is %s in %s",          # is JJ in ATTR
                    "was %s in %s",         # was JJ in ATTR
                    "are %s in %s",         # are JJ in ATTR
                    "were %s in %s",        # were JJ in ATTR
                    "is %s of %s",          # is JJ of ATTR
                    "was %s of %s",         # was JJ of ATTR
                    "are %s of %s",         # are JJ of ATTR
                    "were %s of %s"         # were JJ of ATTR
                    ]

nn_attr_patterns = [
                    
                    ]

def select_attribute(NN, JJ):
    for ATT in attributes:
        