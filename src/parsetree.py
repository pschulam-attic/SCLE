import re
from sys import argv

class ParseTree(object):
    def __init__(self, str):
        self.root = self.build_node(str)

    def __iter__(self):
        self.bfs_queue = []
        self.bfs_queue.append(self.root)
        return self

    def next(self):
        if len(self.bfs_queue) == 0:
            raise StopIteration
        n = self.bfs_queue.pop(0)
        for c in n:
            self.bfs_queue.append(c)
        return n

    @staticmethod
    def build_node(str):
        m = re.match(r'^\((\w+)~(\w+)~\d+~\d+', str)
        parent = node(m.groups()[0], m.groups()[1])
        str = str[m.end():]

        i = 0
        depth = 0
        for c in str:
            if c == '(':
                depth += 1
                if depth == 1:
                    child = ParseTree.build_node(str[i:])
                    parent.children.append(child)
            elif c == ')':
                if depth > 0:
                    depth -= 1
                else:
                    if len(parent.children) == 0:
                        terminals = ParseTree.get_terminals(str[:i])
                        for t,pos in terminals:
                            child = node('TERM', t, pos)
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

class node(object):
    def __init__(self, type, headword, pos=None):
        self.type = type
        self.headword = headword
        if pos:
            self.pos = pos
        self.children = []

    def __iter__(self):
        self.cur_child = 0
        return self

    def next(self):
        if self.cur_child >= len(self.children):
            raise StopIteration
        c = self.children(self.cur_child)
        self.cur_child += 1
        return c

def main():
    pass

if __name__ == "__main__":
    main()
