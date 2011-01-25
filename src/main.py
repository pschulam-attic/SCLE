from tokenizer import Tokenizer
from tagger import Tagger
from chunker import Chunker

tok = Tokenizer('./data/moby_dick.txt')
sents = tok.get_sentences()
print "Tokenized sentences"
tag = Tagger()
sents = tag.tag(sents)
print "Tagged sentences"
chunk = Chunker()
for i in range(10):
    x = chunk.parse(sents[i])
    print x
print "Done"
