'''
Created on Feb 17, 2011

@author: pschulam
'''

def find_adjectives(tree):
    '''
    Search through the parse tree of a sentence and find adjectives.
    When an adjective is found, look at the ancestors to try and determine
    what noun, if any, the adjective is modifying.
    '''
    pairs = []
    for n in tree:
        if n.type == 'TERM' and n.pos == 'JJ':
            path = n.get_ancestor_path()
            for ancestor in path:
                if ancestor.type.startswith('NP'):
                    pairs.append((ancestor.headword,n.headword))
                    break
    for p in pairs:
        print "%s is %s" % p