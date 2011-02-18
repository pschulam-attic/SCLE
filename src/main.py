#!/usr/bin/python
from sys import argv
from stanford_tagger import tag
from parser import parse
from parse_cleaner import clean
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
    clean_file = clean(parsed_file)

    fd = open(clean_file, 'r')
    parse_trees = []
    print "Building parse trees..."
    for line in fd:
        tree = ParseTree(line)
        parse_trees.append(tree)

    for tree in parse_trees:
        find_adjectives(tree)

if __name__ == "__main__":
    main()
