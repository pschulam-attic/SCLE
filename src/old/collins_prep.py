import tokenizer, tagger
from sys import argv

def prep(filename):
    sents = tokenizer.tokenize(filename)
    t = tagger.Tagger()
    sents = t.tag(sents)
    sents = tagger.nltk2collins(sents)
    new_file = filename[:-3] + 'tagged'
    tagger.write_tagged_file(new_file, sents)
    return new_file

def main():
    '''
    Prepares a file for use by the Collins parser.
    The filename provided must end with '.txt'
    '''
    filename = argv[1]
    prep(filename)

if __name__ == "__main__":
    main()
