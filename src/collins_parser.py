from os import system
from sys import argv
from string import split
from timer import print_timing

collins_path = "/Users/pschulam/Desktop/Thesis/src/COLLINS-PARSER/"
events_path = collins_path + "models/model1/events.gz"
parser_path = collins_path + "code/parser"
grammar_path = collins_path + "models/model1/grammar"

@print_timing
def parse(input):
    print "Parsing %s" % input
    output = split(input, '.')[0] + '.model1'
    (system("gunzip -c %s | %s %s %s 10000 1 1 1 1 > %s 2> /dev/null" %
            (events_path, parser_path, input, grammar_path, output)))
    return output

def main():
    files = argv[1:]
    for f in files:
        parse(f)

if __name__ == "__main__":
    main()
