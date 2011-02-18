'''
Created on Feb 17, 2011

@author: pschulam
'''

class ParseNode(object):
    '''
    An item in a ParseTree. Contains information about the node itself,
    a pointer to its parent, and a list of pointers to its children.
    '''
    def __init__(self, type, headword, parent=None, pos=None):
        self.type = type
        self.headword = headword
        if pos:
            self.pos = pos
        self.parent = parent
        self.children = []

    def __iter__(self):
        self.cur_child = 0
        return self

    def next(self):
        if self.cur_child >= len(self.children):
            raise StopIteration
        c = self.children[self.cur_child]
        self.cur_child += 1
        return c

    def get_ancestor_path(self):
        p = self.parent
        path = []
        while p:
            path.append(p)
            p = p.parent
        return path
        