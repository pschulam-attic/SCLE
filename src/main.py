#!/usr/bin/python
from sys import argv
from collins_prep import prep
from parser import parse
from parse_cleaner import clean
from parsetree import ParseTree

def main():
    '''
    Given a filename, process it and extract all relevant
    nouns and adjectives. Should be a .txt file.
    '''
    filename = argv[1]
    print "Tagging file..."
    tagged_file = prep(filename)
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

if __name__ == "__main__":
    main()
