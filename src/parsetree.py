import re
from parsenode import ParseNode

class ParseTree(object):
    '''
    The tree representation of a parsed sentence. 
    '''
    def __init__(self, str):
        self.root = self.build_node(str)

    def __iter__(self):
        self.dfs_stack = []
        self.dfs_stack.append(self.root)
        return self

    def next(self):
        if len(self.dfs_stack) == 0:
            raise StopIteration
        n = self.dfs_stack.pop()
        for c in n:
            self.dfs_stack.append(c)
        return n

    @staticmethod
    def build_node(str):
        #print "Examining: %s" % str
        m = re.match(r'^\((\w+)~([\w\.]+)~\d+~\d+', str)
        parent = ParseNode(m.groups()[0], m.groups()[1])
        str = str[m.end():]

        i = 0
        depth = 0
        for c in str:
            if c == '(':
                depth += 1
                if depth == 1:
                    child = ParseTree.build_node(str[i:])
                    child.parent = parent
                    parent.children.append(child)
            elif c == ')':
                if depth > 0:
                    depth -= 1
                else:
                    if len(parent.children) == 0:
                        terminals = ParseTree.get_terminals(str[:i])
                        for t,pos in terminals:
                            child = ParseNode('TERM', t, parent, pos)
                            parent.children.append(child)
                    return parent
            i += 1

        # Should never get here
        assert 0

    @staticmethod
    def get_terminals(str):
        result = []
        terminals = str.split()
        for t in terminals:
            pair = t.split('/')
            result.append(pair)
        return result
