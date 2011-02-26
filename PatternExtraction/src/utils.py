from __future__ import division
from operator import itemgetter, add
import random
import re
import config

from datetime import timedelta, datetime
from dateutil.relativedelta import *

__author__ = "Vera Sheinman"

def ByStrLength():
    def compare(str1, str2): return cmp(len(str1), len(str2))
    return compare

def ByColumn(key):
   def compare(obj1, obj2): return cmp(obj1[key], obj2[key])
   return compare

def ByAttribute(name):
   def compare(obj1, obj2): return cmp(getattr(obj1, name), getattr(obj2, name))
   return compare 

def ByAttributes(names = []):
    """
    given a list of attribute names, will sort first by first name, then by second
    and so forth
    """
    def compare(obj1, obj2):
        res = 0
        for i in range(0, len(names)):
            if res == 0:
                res = cmp(getattr(obj1, names[i]), getattr(obj2, names[i]))
        return res
    return compare
    
def ByComparators(comparators = []):
    """Given a list of comparator functors, first sort by first, then by second, 
    and so forth.
    """
    def compare(obj1, obj2):
        res = 0
        for i in range(0, len(comparators)):
            if res == 0:
                res = comparators[i](obj1, obj2)
        return res
    return compare
  
def sort_by_val(hash, reverse=False):
    """
    receive dictionary
    return keys, values list sorted by values
    """
    items = hash.items()
    items.sort(ByColumn(1), reverse = reverse)
    return items

def reverse_list(list):
    rlist = list[:]
    rlist.reverse()
    return rlist

def compare_lists(list1, list2):
    # consider utilizing python's "set"
    dif1 = [item for item in list1 if item not in list2]
    dif2 = [item for item in list2 if item not in list1]
    if len(dif1) == 0 and len(dif2) == 0:
        return True
    else:
        return False

def exchange(o1, o2):
    temp = o1
    o1 = o2
    o2 = temp

def random_int(x, y):
    return random.randint(x,y)

def shuffle(list):
    shuffled = list[:]
    random.shuffle(shuffled)
    return shuffled

def random_join(to_join = [], separators = []):
    """
    performs join each time using a random separator from the list
    returns a string
    assumption: the provided list of separators takes into account all the needed spaces
    no spaces are added by this routine
    example:
    given to_join = ['hello', 'dear', 'friends']
          separators = [" ha-ha ha ", " ho ho ", " heee "]
    might return: "hello ha-ha ha dear heee friends"
    or: "hello heee dear heee friends"
    etc..
    """
    joined_ar = []
    max = len(to_join)
    for index in range(0, max):
        if index < max:
            joined_ar.append("%s%s" % (to_join[index], random.choice(separators)))
        else:
            joined_ar.append("%s" % to_join[index])
    joined_str = "".join(joined_ar)
    return joined_str

def sum(list):
    sum = 0
    if len(list) > 0:
        sum = reduce(add, list)
    return sum

def divide(num = 0, denom = 0):
    """
    divide numerator by denominator
    if denominator is 0 return 0
    """
    result = 0
    if denom > 0:
        result = (num / denom)
    return result


def add_to_dict(dict = {}, key = "", add = 1, init_val = 0):
    """
    if key in dict update the dict[key] and increase it by val
    otherwise initialize the dict by the init_val
    """
    
    if key in dict:
        dict[key] = dict[key] + add
    else:
        dict[key] = init_val
        
def add_to_nested_dict(dict = {}, keys = ("", ""), add = 1, init_val = 0):
    """
    expected dict of the type:
    {key : {key : value}}
    keys[0] - key in the given dict
    keys[1] - inernal key in the nested dict dict[key[0]]
    """
    if not keys[0] in dict:
        dict[keys[0]] = {}
    add_to_dict(dict = dict[keys[0]], key = keys[1], add = add, init_val = init_val)
        
def clean_word(word):
        """ gets rid of WN additions to words like: quasi(a) 
        For input: word(x) - Return: word
        For input: wo_rd - Return: wo-rd
        For input: word - Return: word
        """
        pattern = re.compile('(.*)\(.+\)')
        search = pattern.search(word)
        clean_word = word
        if search:
            clean_word = search.group(1)
        clean_word = re.sub("_", '-', clean_word) 
        return clean_word



def get_num_from_file(from_file = ""):
    """
    return the last number in the file
    """
    f = open(from_file, 'r')
    num = 0
    for line in f:
        num = int(line)
    f.close()
    return num

def append_num_to_file(num = 0, to_file = ""):
    """append the given number as the last line in the given to_file
    """
    fw = open(to_file, 'a')
        
    fw.write("\n%d" % num)
    fw.close()
    
def get_dict_from_file(pattern = "", from_file = ""):
    """
    assume pattern with two groups, first hashable, second integer
    return dictionary:
    dict[group0] = group1
    """
    f = open(from_file, 'r')
    res_dict = {}
    for line in f:
        match = re.search(pattern, line)
        if match:
            res_dict[match.group(1)] = int(match.group(2))
    f.close()
    return res_dict


def put_dict_to_file(dict = {}, to_file = ""):
    fw = None
    fw = open(to_file, 'w')
    result = ["%s - %d" % (item, dict[item]) for item in dict.keys()]
        
    fw.write("\n".join(result))
    fw.close()

def big_number_format(num = 0):
    numstr = str(num)
    #turn into array and reverse
    numlist = []
    decimal_flag = False
    remains = []
    for letter in numstr:
        if letter == ".":
            decimal_flag = True   
            remains.append(letter)
        elif decimal_flag:
            remains.append(letter) 
        elif not decimal_flag:
            numlist.append(letter)
        
    numlist.reverse()
    
    # stick commas every three digits
    res = []
    for index in range(len(numlist)):
        if index > 0 and index % 3 == 0:
            res.append(",")
        res.append(numlist[index])
    
    # reverse back and put back into string
    res.reverse()
    res.extend(remains)
    numstr = "".join(res)
    
    return numstr

def mutually_exclusive(set = [], another_set = []):
    mutually_exclusive = True
    for item in set:
        if item in another_set:
            mutually_exclusive = False
    return mutually_exclusive

def print_debug(message = "", allowed = config.DEBUG, level = 0):
    if allowed > level:
        print message

def get_corpus_sentences(from_file):
    f = open(from_file, 'r')
    lines = []
    for line in f:
        str_line = line[:]
        str_line = str_line.rstrip()
        lines.append(str_line)
    f.close()
    return lines

def append_to_file(lines = [], to_file = "append_file.txt"):
    f = open(to_file,  'a')
    for line in lines:
        f.write("%s" % line)
    f.close()


def print_time_stamp(start):
     end = datetime.now()  
     print "from %s to %s (total: %s)" % (start, end, end - start)

def get_text_from_file(from_file, join_sep = ""):
    """
    join_sep -- by what character to join all the lines (default: empty)
    """
    f = open(from_file, 'r')
    lines = []
    for line in f:
        str_line = line[:]
        lines.append(str_line.rstrip())
    result = join_sep.join(lines)
    f.close()
    return result
def read_wordlist(from_file):
    f = open(from_file, 'r')
    words = []
    for line in f:
        str_line = line[:]
        word = str_line.strip()   
        words.append(word)
    return words     

def test():
    
   
   list = ["hello", "world", "test"]
   separators = [" * ", " * * ", " * * * "]
   str = random_join(to_join = list, separators = separators)
   print str
   
   dict = {'hello' : {'some' : 5}, 'beautiful' : {'some' : 0}}
   keys = dict.keys()
   keys.sort(ByComparators([ByStrLength()]))
   print keys
   
   num = 100000000000
   print big_number_format(num = num)
   

if __name__ == "__main__":
    test()
