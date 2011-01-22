"""
source: http://www.mail-archive.com/python-list@python.org/msg89034.html
with minor modifications
"""

class nkRange(object):
    def __init__(self, n, k):
        self.n = n
        self.k = k
        self.l = n - k + 1
        self.__indexer = range(0, k)
        self.__vector = range(1, k+1)
        self.__last = range(self.l, n+1)
        self.__current_index = 0
        
    def __iter__(self):
        return self

    def next(self):
        if self.__vector == self.__last:
            raise StopIteration
        if self.__current_index > 0:
            idx = self.__get_next_lexico_index()
            self.__increment_vector(idx)
        self.__current_index += 1
        return self.__vector

    def __get_next_lexico_index(self):
        high_value = -1
        high_index = -1
        for i in self.__indexer:
            val = self.__vector[i]
            if val > high_value and val < self.l + i:
                high_value = val
                high_index = i
        return high_index

    def __increment_vector(self, index):
        a_index = self.__vector[index]
        for i in range(self.k - index):
            self.__vector[i+index] = a_index + i + 1            

def permutation(lst):
    queue = [-1]
    lenlst = len(lst)
    while queue:
        i = queue[-1]+1
        if i == lenlst:
            queue.pop()
        elif i not in queue:
            queue[-1] = i
            if len(queue) == lenlst:
                yield [lst[j] for j in queue]
            queue.append(-1)
        else:
            queue[-1] = i

def kSubsets( alist, k ):
    n = len(alist)
    for vector in nkRange(n, k):
        ret = []
        for i in vector:
            ret.append( alist[i-1] )
        yield ret
          
