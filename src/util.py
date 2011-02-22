'''
Created on Feb 18, 2011

@author: pschulam
'''

from string import split

def clean_parse(filename):
    out_file = split(filename, '.')[0] + '.clean' 
    input = open(filename, 'r')
    output = open(out_file, 'w')
    for line in input:
        if line.startswith("(TOP~"):
            output.write(line)
    input.close()
    output.close()
    return out_file
