#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import utils
import config

class Pattern():
    '''
    Represents a structure of a single pattern of the form:
    [PREFIX WORDS] SEED1 [INFIX WORDS] SEED2 [INFIX WORDS] SEED3 ... SEEDn [POSTFIX WORDS]
    '''
    SLOT_NAME = "seed"
    def __init__(self, prefix = [], infixes = [[]], postfix = [], slot_name = SLOT_NAME):
        self.prefix = prefix[:]
        self.infixes = []
        for infix in infixes:
            self.infixes.append(infix[:])
        self.postfix = postfix[:]
        self.slot_name = slot_name
    
    def to_str(self, no_index = False, special_slot_name = ""):
        '''
        @param no_index: if True all the slots will be initiated with the same slot name
        '''
        index = 1
        if no_index:
            seed_name = special_slot_name
        else:
            seed_name = "%s_%d" % (self.slot_name, index)
        internals = [seed_name]
        
        for infix in self.infixes:
            index = index + 1
            if no_index:
                seed_name = special_slot_name
            else:
                seed_name = "%s_%d" % (self.slot_name, index)
        
            internals.extend(infix)
            internals.append(seed_name)
        
        internal_string = " ".join(internals)    
        string = "%s %s %s" % (" ".join(self.prefix), 
                               internal_string, 
                               " ".join(self.postfix))
        # trimming white spaces
        string = string.lstrip()
        string = string.rstrip()
        return string
    
    def to_query(self):
        query = self.to_str(no_index = True, special_slot_name = "*")
        return query
    
    def __str__(self):
        return self.to_str(no_index = False)
    
    def __eq__(self, other):
        if self.__str() == other.__str:
            return True
        else:
            return False
    
    def is_binary(self):
        if len(self.infixes) == 1:
            return True
        else:
            return False
    
    
    def init_pattern_from_string(self, pattern_string = "", slot_name = SLOT_NAME):
        '''
        Given a string construct initialize this pattern from it
        Assume the string doesn't include punctuation, only space separated words
        '''
        self.slot_name = slot_name
        self.prefix = []
        self.infixes = []
        self.postfix = []
        
        words = pattern_string.split(" ")
        
        regex = "\w*_\d"
        slot_pattern = re.compile(regex)
       
        infixes_index = -1
        append_word = True
        
        for word in words:
            if slot_pattern.match(word):
                infixes_index = infixes_index + 1
                append_word = False
                if infixes_index > 0:
                    self.infixes.append(self.postfix[:])
                self.postfix = []
            else:
                append_word = True
            if infixes_index < 0:
                self.prefix.append(word)
            elif append_word:
                self.postfix.append(word)
        
        
      
    def pattern_string_instance(self, instance_values = []):
        '''
        @return a string of this pattern instantiated with given values in its slots.
        
        @param instance_values: list of values to put in the slots of the pattern
                               !the size of the list has to correspond with the number
                                of slots in this pattern
        
        Example: for pattern prefix = [very], infix = [and] 
                 instance values = [big, huge]
                 return - "very big and huge"
        '''
        
        index = 0
        internals = []
        if len(instance_values) > index:    
            internals.append(instance_values[index])
        
        for infix in self.infixes:
            index = index + 1
            internals.extend(infix)
            internals.append(instance_values[index])
        
        internal_string = " ".join(internals)    
        string = "%s %s %s" % (" ".join(self.prefix), 
                               internal_string, 
                               " ".join(self.postfix))
        # trimming white spaces
        string = string.lstrip()
        string = string.rstrip()
        return string
    
    def get_words(self):  
        '''
        @return a set of words that appear in pattern
        '''          
        words = set()
        for item in self.prefix:
            words.add(item)
        for infix in self.infixes:
            for item in infix:
                words.add(item)
        for item in self.postfix:
            words.add(item)
        return words
        
            
            
        
            
    
class PatternExtractor():
    '''
    Extracts patterns of the form:
    [PREFIX WORDS] SEED1 [INFIX WORDS] SEED2 [INFIX WORDS] SEED3 ... SEEDn [POSTFIX WORDS]
    
    Patterns are extracted from a corpus of sentences.
    Each pattern is within a sentence.
    '''
    
    def __init__(self, max_prefix_size = 3, max_postfix_size = 3,
                 max_infix_sizes = [0]):
        self.max_prefix_size = max_prefix_size # maximal number of words in a prefix
        self.max_postfix_size = max_postfix_size
        self.max_infix_sizes = max_infix_sizes # maximal sizes for infixes
    
    def _build_regex_for_pattern(self, seeds = [], prefix_size = 0, infix_sizes = [0],
                                 postfix_size = 0):
        # building regex 
        regex_word = "(\w+)"
        regex_delimiter = " "
        regex_list = []
        for index in range (0, prefix_size):
            regex_list.append(regex_word)
        for index in range(0, len(infix_sizes)):
            regex_list.append(seeds[index])
            for local_index in range(0, infix_sizes[index]):
                regex_list.append(regex_word)
        # add the last seed
        regex_list.append(seeds[-1])  
        for index in range(0, postfix_size):
            regex_list.append(regex_word)
        
        regex = regex_delimiter.join(regex_list)
        return regex
    
    def extract_pattern_from_sentence(self, sentence, seeds = [], prefix_size = 0, 
                                      infix_sizes = [0], postfix_size = 0):
        '''
        Extract a single pattern from a single sentence, by parameters of prefix, 
        infix and postfix sizes.
        
        Assumption: each pattern appears in a sentence maximum once! 
        (that's how it will be counted for frequency)
        
        @return a Pattern or None if no such pattern was detected
        ''' 
        
        regex = self._build_regex_for_pattern(seeds = seeds, 
                                              prefix_size = prefix_size,
                                              infix_sizes = infix_sizes, 
                                              postfix_size = postfix_size)
        regex_pattern = re.compile(regex)
        match = regex_pattern.search(sentence)
        pattern = None
        if match:
            prefix = []
            all_infixes = []
            postfix = []
            
            #prefix
            for index in range(0, prefix_size):
                prefix.append(match.groups()[index])
            last_group = prefix_size
            
            #infixes
            for infix in infix_sizes:
                infixes = []
                for index in range(last_group, infix + last_group):
                    infixes.append(match.groups()[index])
                last_group = last_group + infix
                all_infixes.append(infixes[:])
            
            #postfix
            for index in range(last_group, postfix_size + last_group):
                postfix.append(match.groups()[index])
            
            pattern = Pattern(prefix = prefix, infixes = all_infixes, postfix = postfix)
        return pattern
    
    def _store_pattern_in_dict(self, pattern = None, patterns = {}):
        '''
        Stores a string representation of a given pattern in the given patterns hash.
        Counts the number of instances.
        '''
        if pattern:
            #hashable
            str_pattern = str(pattern)
            if str_pattern in patterns:
                patterns[str_pattern] = patterns[str_pattern] + 1
            else:
                patterns[str_pattern] = 1
        return
          
    def extract_patterns(self, sentences = [], seeds = []):
        '''
        Given a set of sentences and a set of seeds, extract the patterns with
        in which the given seeds appear.
        
        @param sentences: a list of sentences, the corpus to search the patterns in.
        @param seeds: a list of words that have to be contained in the patterns
        
        string representations of the patterns are stored as the returned dictionary keys
        
        @return dictionary of patterns and their frequency of appearance
        '''
        patterns = {}
        
        # initialize to [0, 0, 0, ...]
        sizes = []
        # initialize for all infixes + prefix + postfix
        for index in range(0, len(self.max_infix_sizes) + 2):
            sizes.append(0)
        
        end_of_list = False
        max_values = [self.max_prefix_size, self.max_postfix_size]
        max_values.extend(self.max_infix_sizes)
        while not end_of_list:
            for sentence in sentences:
                pattern = self.extract_pattern_from_sentence(sentence = sentence, 
                                                             seeds = seeds, 
                                                             prefix_size = sizes[0], 
                                                             infix_sizes = sizes[2:], 
                                                             postfix_size = sizes[1])
                self._store_pattern_in_dict(pattern = pattern, patterns = patterns)
                
            (sizes, end_of_list) = self._increment_list(list = sizes, 
                                                        max_vals = max_values,
                                                        init_val = 0, 
                                                        step = 1)
        return patterns
    
    def build_search_query(self, seeds = [], infix_sizes = [], wildcard = "*"):
        ''' 
        Build a single query to search the appropriate sentences in a corpus.
        Each query is a combination of seed words and wildcards in between them
        Join is using space
        Returned query is wrapped in quotes and spaces " query "
        
        @param seeds: the seed words to be put in the query slots
        @param infix_sizes: a list of number of wildcard characters to put after the 
                      corresponding seed from the seeds list
        @param wildcard: the character/string to be used as the wildcard 
        
        Example:
        input parameters - seeds = ['a', 'b']
                           infix_sizes = [1]
                           wildcard = '*'
        query string " a * b "
        
        @return a query string
        '''
        query_items = []
        for index in range(0, len(infix_sizes)):
            query_items.append(seeds[index])
            for infix_size in range(0, infix_sizes[index]):
                query_items.append(wildcard)
        # add the last seed item
        query_items.append(seeds[-1])
        
        query_string = " ".join(query_items)
        # wrap the query
        query = "\" %s \"" % (query_string)
        
        return query
    
    def _increment(self, val = 0, max_val = 0, init_val = 0, step = 1):
        '''
        Increment the given value by step not exceeding the max_val.
        
        @param val: the value to increment
        @param max_val: the maximum value this value can reach, 
        @param init_val: the initial value. the value will be reset to this value if it reaches the max_val
        @param step: a single incrementation step 
        
        @return the incremented value
        '''
        if val < max_val:
            return val + step
        else:
            return init_val
    
    def _increment_list(self, list = [], max_vals = [], init_val = 0, step = 1):
        '''
        Increment a the appropriate value in the given list
        
        Examples:
        1) input values - list = [0, 0, 0], max_vals = [0, 0, 1], init_val = 0, step = 1
           output - list = [0, 0, 1]
        2) input values - list = [0, 0, 1], max_vals = [1, 1, 1], init_val = 0, step = 1
           output - list = [0, 1, 0]
        @return a pair:
        incremented_list - a list with the necessary values incremented
        end_of_list - a boolean regarding whether or not it is possible to increment further
        '''
        continue_to_increment = True
        current_index = -1
        incremented_list = list[:] # copy of the list
        end_of_list = False
        
        while continue_to_increment and  current_index >= -1 * len(max_vals):
            prev_val = incremented_list[current_index]
            new_val = self._increment(prev_val, max_vals[current_index], init_val, step)
            incremented_list[current_index] = new_val
            
            if new_val > prev_val:
                continue_to_increment = False
                end_of_list = False
            else:
                current_index = current_index -1
        
        if continue_to_increment:
            end_of_list = True
        
        return (incremented_list, end_of_list)

    
    def build_search_queries(self, seeds = []):
        '''
        Iterate over all the maximal values (self.max_infix_sizes) 
        and produce all possible search queries in terms of num. of wild cards.
        
        @param seeds: a list of seeds that will participate in the extracted pattern
        
        @return a list of search queries to extract appropriate sentences from a corpus
        '''
        queries = []
        
        # initialize to [0, 0, 0, ...]
        sizes = []
        for index in range(0, len(self.max_infix_sizes)):
            sizes.append(0)
        
        iteration_indexes = range(0, len(self.max_infix_sizes))
        end_of_list = False
        while not end_of_list:
            queries.append(self.build_search_query(seeds = seeds, infix_sizes = sizes[:]))
            (sizes, end_of_list) = self._increment_list(list = sizes, 
                                                        max_vals = self.max_infix_sizes, 
                                                        init_val = 0, 
                                                        step = 1)
            
        return queries
          
        
        
from web_search import *

class CorpusExtractor():
    ''' 
    Create a corpus, based on given criteria. 
    Basically extract sentences from the snippets from a web search using Yahoo
    
    '''  
    def __init__(self, we = None):
        if we:
            self.web_extractor = we
        else:
            self.web_extractor = YahooExtractor(lang=config.LANGUAGE)
    
    def queries_for_pattern(self, instances = [], slot_name = "", 
                            pattern_strings = []):
        '''
        @return all the queries for the given pattern string, using the given instances
        
        assumption: given pattern_string stand for binary patterns
        instances -- a list of items to be put as the known instance in the pattern slots
        
        @rtype  a list of strings (queries)
        '''
        pattern_queries = []
        for pattern_string in pattern_strings:
            pattern = Pattern()
            pattern.init_pattern_from_string(pattern_string, slot_name)
            
            for instance in instances:
                pattern_queries.append(pattern.pattern_string_instance(instance_values = 
                                                                       [instance, "*"]))
                pattern_queries.append(pattern.pattern_string_instance(instance_values = 
                                                                       ["*", instance]))
        return pattern_queries
    
    def get_corpus_for_queries(self, queries = [], instances = []):
        '''
        queries -- a list of queries to retrieve the sentences for
        Return list of sentences that contain the patterns from the web
        '''
        corpus = []
        for query in queries:
            sentences = self.retrieve_sentences(query, min_sentence_len = 10,
                                            conditions = instances,
                                            conditions_aggr = "OR")
            sentences = self.clean_sentences(sentences)
            corpus.extend(sentences)
        return corpus
    
    def get_corpus_for_patterns(self, patterns = [], slot_name = ""):
        '''
        acquire sentences corpus for given patterns from the web
        
        @param patterns: list of strings representing patterns
        @param slot_name: the slot_name used in the string representation of the patterns
        
        @return: list of sentences that contain the patterns from the web
        '''
        corpus = []
        for pattern_string in patterns:
            
            pattern = Pattern()
            pattern.init_pattern_from_string(pattern_string, slot_name)
            query = pattern.to_query()
            words = pattern.get_words()
            
            sentences = self.retrieve_sentences(query, min_sentence_len = 10,
                                                conditions = words)
            sentences = self.clean_sentences(sentences)
            corpus.extend(sentences)
        return corpus
            
       
    def retrieve_sentences(self, query = "",
                           min_sentence_len = -1,
                           conditions = [],
                           conditions_aggr = "AND"):
        '''
        retrieve all the sentences with length bigger than min_sentence_len
        @param conditions: a list of a set of words that have to be in the final sentences choice
        @return a list of sentences
        '''
        if config.DEBUG > 1:
            print "Extracting sentences corpus, searching for %s" % query
        max_pages = 100
        max_page_sets = 10
        sentences = []
        
        for i in range(0,max_page_sets):
            start = max_pages*i + 1
            summaries = self.web_extractor.retrieve_summaries(query, 
                                                              start = start, 
                                                              pages = max_pages)
            
            for summary in summaries:
                
                # put everything in lower case
                sentences_in_summary = summary.lower().split(".")
                for sentence in sentences_in_summary:
                    append_me = True
                    if len(sentence) > min_sentence_len:
                        if conditions_aggr == "AND": #AND
                            for condition in conditions:
                                if not condition in sentence:
                                    append_me = False
                        else: # OR
                            append_me = False
                            for condition in conditions:
                                if condition in sentence:
                                    append_me = True
                        if append_me:
                            sentences.append(sentence)
        
        print sentences
        return sentences
    
    def clean_sentences(self, sentences = [], 
                        clean_chars = "\s,.:;><\/|!?#$%^&*()-=+\"\'_"):
        """
        Substitute any combination of the given characters in the 
        given sentences by a single space.
        
        @param sentences :  a list of sentences for cleaning
        @param clean_chars:   a string of characters that have to be cleaned out
        
        @return: a list of cleaned sentences
        """
        clean_sentences = []
        regex = re.compile("[%s]+" % clean_chars)
        for sentence in sentences:
            clean_sentence = regex.sub(" ", sentence)
            clean_sentences.append(clean_sentence)
        return clean_sentences
            
            
        

class PatternOutput(): 
    '''
    Structure to hold the representation of an extracted pattern for evaluation
    '''
    def __init__(self, pattern = "", seeds_dict = {}):
        self.pattern = pattern
        self.strlen = len(pattern)
        self.num_of_seeds = len(seeds_dict)
        self.seeds_dict = seeds_dict
        self.max_seed = max(self.seeds_dict.values())
        self.avg_seed = utils.divide(grad_utils.sum(self.seeds_dict.values()), 
                                                    self.num_of_seeds)
                
    def _reverse_str_list(self, str = ""):
        '''
        Reverse an array that is represented as list
        @return: a string representing a reverse array
        '''
        res_list = []
        strlist = str[1:-1]
        items = strlist.split(", ")
        for item in items:
            res_list.append(item[1:-1])
        reverse_list =  []
        for item in reversed(res_list):
            reverse_list.append(item)
        return "%s" % reverse_list
    
    def add_seeds_dict(self, seeds_dict = {}):
        '''
        Add frequencies from the given seeds_dict to the local seeds_dict
        new keys are simply added to the seeds_dict dictionary
        for existing keys values are summed.
        
        @param seeds_dict: a dictionary of seeds and their frequencies of appearance
        
        @return: nothing, the changes are made for this PatternOutput instance
        '''
        for seed in seeds_dict:
            if seed in self.seeds_dict:
                self.seeds_dict[seed] = self.seeds_dict[seed] + seeds_dict[seed]
            else:
                self.seeds_dict[seed] = seeds_dict[seed]
        
    
        
    def __str__(self):
        string = "%s : %s" % (self.pattern, self.seeds_dict)
        return string

def get_me_patterns(seeds_sets = [], extractor = None, threshold = 2):
    '''
    threshold -- the minimum number of appearances for a pattern to enter the results
    '''
    corpus = CorpusExtractor()
    all_in_patterns = {}
    pattern_records = []
    
    for set in seeds_sets:
        patterns = {}
        queries = extractor.build_search_queries(seeds = set)
        
        
        sentences = [] # clean the previous sentences not to check them again for patterns
        for query in queries:
            sentences.extend(corpus.retrieve_sentences(query))
        
        sentences = corpus.clean_sentences(sentences = sentences)
        patterns = extractor.extract_patterns(sentences = sentences, seeds = set)
        for key in patterns:
            if patterns[key] > threshold:
                if key in all_in_patterns:
                    all_in_patterns[key][str(set)] = patterns[key]
                else:
                    all_in_patterns[key] = {}
                    all_in_patterns[key][str(set)] = patterns[key]
    return all_in_patterns

def get_sorted_pattern_records(patterns = [], sort_attributes = []):
    '''
    Given patterns construct the corresponding pattern records and sort them by given attributes
    '''
    pattern_records = []
    
    for pattern in patterns:
        pattern_output = PatternOutput(pattern = pattern, seeds_dict = patterns[pattern])
        # append only the patterns supported by more than one seed
        if len(pattern_output.seeds_dict) > 0:
            pattern_records.append(pattern_output)
    pattern_records.sort(utils.ByAttributes(sort_attributes), 
                         reverse = True)
    
    return pattern_records
    
def output_patterns(ab_patterns = [], ba_patterns = [], 
                    ab_pattern_records = [], ba_pattern_records = [],
                    intersection_file = "intersection.txt",
                    unique_ab_file = "unique_ab.txt",
                    unique_ba_file = "unique_ba.txt"):
    '''
    Assume sorted ab_pattern_records and ba_pattern_records
    '''
    
    fw = open(intersection_file, 'a')
    fw_unique = open(unique_ab_file, 'a')
    print "Writing Intersection and Unique AB"
    for pattern in ab_pattern_records:
        if pattern.pattern in ba_patterns:
            inter_seeds = {}
            for ba_pattern in ba_pattern_records:
                if ba_pattern.pattern == pattern.pattern:
                    pattern.add_seeds_dict(seeds_dict = ba_pattern.seeds_dict)
                    fw.write("%s\n" % str(pattern))
        # Unique AB
        else:
            fw_unique.write("%s\n" % str(pattern))
    fw.close()
    fw_unique.close()
     
    fw = open(unique_ba_file, 'a')
    print "Writing Unique BA"
    for pattern in ba_pattern_records:
        if pattern.pattern not in ab_patterns:
            fw.write("%s\n" % str(pattern))
    fw.close()

def run(seeds_sets=[]):
    print "Running pattern extraction"
    reverse_sets = []
    for set in seeds_sets:
        rset = utils.reverse_list(set)
        reverse_sets.append(rset)
    
    extractor = PatternExtractor(max_prefix_size = 2,
                                 max_infix_sizes = [2],
                                 max_postfix_size = 2)
    
    ab_patterns = get_me_patterns(seeds_sets = seeds_sets, extractor = extractor)
    ba_patterns = get_me_patterns(seeds_sets = reverse_sets, extractor = extractor)
    
    sort_attributes = ['num_of_seeds', 'avg_seed', 'strlen']
    pattern_records = get_sorted_pattern_records(patterns = ab_patterns, 
                                                 sort_attributes = sort_attributes)

    ba_pattern_records = get_sorted_pattern_records(patterns = ba_patterns, 
                                                    sort_attributes = sort_attributes)
    
    output_patterns(ab_patterns = ab_patterns, ba_patterns = ba_patterns,
                    ab_pattern_records = pattern_records, ba_pattern_records = ba_pattern_records,
                    intersection_file = "../patterns/intersection.txt",
                    unique_ab_file = "../patterns/unique_ab.txt",
                    unique_ba_file = "../patterns/unique_ba.txt")
    

if __name__ == "__main__":
    bin_sets = [['big', 'huge'], ['cold', 'frigid'], ['tiny', 'infinitesimal'],
                  ['old', 'ancient'], ['middle-aged', 'old'], ['good', 'wonderful'],
                  ['middle-aged', 'ancient'], ['huge', 'astronomical'], 
                  ['young', 'infantile'], ['evil', 'fiendish']]
    
    run(seeds_sets = bin_sets[:])