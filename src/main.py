#!/usr/bin/python
from string import split
from sys import argv
from stanford_tagger import tag
from collins_parser import parse
from util import clean_parse
from parsetree import ParseTree
from adjfinder import find_adjectives

def main():
    '''
    Given a filename, process it and extract all relevant
    nouns and adjectives. Should be a .txt file.
    '''
    filename = argv[1]
    print "Tagging file..."
    tagged_file = tag(filename)
    print "Parsing file..."
    parsed_file = parse(tagged_file)
    print "Cleaning parsed file..."
    clean_file = clean_parse(parsed_file)

    fd = open(clean_file, 'r')
    parse_trees = []
    print "Building parse trees..."
    for line in fd:
        tree = ParseTree(line)
        parse_trees.append(tree)

    out_file = split(clean_file, '.')[0] + '.out'
    find_adjectives(parse_trees, out_file)

if __name__ == "__main__":
    main()
