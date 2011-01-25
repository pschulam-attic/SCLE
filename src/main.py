from tokenizer import Tokenizer
from tagger import Tagger
from chunker import Chunker

tok = Tokenizer()
t = Tagger()
c = Chunker()

sents = tok.tokenize('data/moby_dick.txt')
sents = t.tag(sents)
sents = c.chunk(sents)
