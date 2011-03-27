'''
Created on Feb 17, 2011

@author: pschulam
'''

def noun_phrase(n, path):
    for ancestor in path:
        if ancestor.type.startswith('NP'):
            return (ancestor.headword, n.headword)

def subordinating_conjunction(n, path):
    for ancestor in path:
        if ancestor.type == 'SBAR':
            p = ancestor.parent
            for c in p:
                if (c.type.startswith('NP') and not c.headword == 'that'):
                    return (c.headword, n.headword)

def connecting_verb(n, path):
    for ancestor in path:
        if ancestor.type == 'S':
            for c in ancestor:
                if c.type.startswith('NP') and not c.headword == 'that':
                    return (c.headword, n.headword)

def build_concepts(pairs):
    concepts = {}
    for n,a in pairs:
        if n in concepts.keys() and a not in concepts[n]:
            concepts[n].append(a)
        else:
            concepts[n] = [a]
    return concepts

def clean_concepts(concepts):
    pass

def in_blacklist(adj):
    blacklist = ['inner',
                 'outer',
                 'some',
                 'many',
                 'most',
                 'all',
                 'few',
                 'same',
                 'equivalent',
                 'other',
                 'numerous',
                 'various']
    for w in blacklist:
        if adj == w:
            return True
    return False

def find_adjectives(trees, out_file=None):
    '''
    Search through the parse tree of a sentence and find adjectives.
    When an adjective is found, look at the ancestors to try and determine
    what noun, if any, the adjective is modifying.
    '''
    methods = [noun_phrase,
               subordinating_conjunction,
               connecting_verb]
    pairs = []
    for t in trees:
        for n in t:
            if n.type == 'TERM' and n.pos == 'JJ' and not in_blacklist(n.headword):
                path = n.get_ancestor_path()
                p = None
                for m in methods:
                    p = m(n, path)
                    if p:
                        break
                if p:
                    pairs.append(p)
    concepts = build_concepts(pairs)
    if out_file:
        f = open(out_file, 'w')
        for k, v in concepts.items():
            for a in v:
                f.write("%s,%s\n" % (k,a))
        f.close()
    else:
        for k, v in concepts.items():
            for a in v:
                print "%s is %s" % (k, a)
