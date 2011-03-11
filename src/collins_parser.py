from os import system
from sys import argv
from string import split

collins_path = "/home/pschulam/Documents/SCLE/src/COLLINS-PARSER/"
events_path = collins_path + "models/model1/events.gz"
parser_path = collins_path + "code/parser"
grammar_path = collins_path + "models/model1/grammar"

def parse(input):
    output = split(input, '.')[0] + '.model1'
    (system("gunzip -c %s | %s %s %s 10000 1 1 1 1 > %s" %
            (events_path, parser_path, input, grammar_path, output)))
    return output

def main():
    if len(argv) != 2:
        print "Specify input file and output file"
    else: 
        parse(argv[1])

if __name__ == "__main__":
    main()
