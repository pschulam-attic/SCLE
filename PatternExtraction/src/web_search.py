from yahoo.search.web import WebSearch

import utils
import config
from combs import *

PAGES = 10
START = 1
YAHOO_API = "Vera.Sheinman.Key"

__author__ = "Vera Sheinman"

class WebExtractor():
    
    __version__ = 0
    
    def __init__(self, type='phrase', lang= config.LANGUAGE, 
                 pages=PAGES, search=None, debug = False):
        self.type = type
        
        self.srch = search
        if self.srch:
            self.srch.results = pages
            self.srch.language = lang
            self.srch.type = type
        
        self.debug = debug
           
    
    def __wrap_query(self, query):
        return "\"%s\"" % query
    
    def get_proximity_query(self, list, pstr):
        proximity = " %s " % pstr
        query = proximity.join(list)
        return self.__wrap_query(query)
    
    
    def get_alternative_proximity_query(self, list, pstr):
        """
        Note the non-deterministic nature of this routine
        the basic proximity query with a single wildcard is always present 
        """
        none = " "
        one = " %s " % pstr
        two = " %s %s " % (pstr, pstr)
        three = " %s %s %s " % (pstr, pstr, pstr)
        query_none = self.__wrap_query(none.join(list))
        query_one = self.__wrap_query(one.join(list))
        
        query_two = self.__wrap_query(utils.random_join(to_join = list,
                                                             separators = [none, one, two, three]))
        query_three = self.__wrap_query(utils.random_join(to_join = list,
                                                             separators = [none, one, two, three]))
        final_query = "%s OR %s OR %s OR %s" % (query_none, query_one, query_two, query_three)
        if self.debug:
            print "final query %s" % final_query
        return final_query
        
    def get_cooc_query(self, list):
        wrapped_items = [self.wrap_query(item) for item in list]
        query = " ".join(wrapped_items)
        return query    
    
    
    def search(self):
        return None
    
    def get_count(self, results, cached=False):
        return 0
    
    def get_results(self, query, start = START, pages  = PAGES, cached=False):
        return None
    
    def get_snippets(self, results, cached=False):
        return None
    
    def wrap_query(self, query):
        """
        query - string of ready-made query word or phrase
        return +"query"
        """
        return "+\"%s\"" % query
    
    def add_context_to_query(self, query = "", context = []):
        """
        query - string of an existing query
        context - list of words to add as context
        return - +"query" +"context_word1" +"context_word2"
        """
        add_queries = []
        for context_word in context:
            add_queries.append(self.wrap_query(context_word))
        context_query = " ".join(add_queries) 
        return "%s %s" % (query, context_query)
        
    
    
        
class YahooExtractor(WebExtractor):
     
    def __init__(self, type='phrase', lang=config.LANGUAGE, 
                 pages=PAGES, search=None):
        srch = WebSearch(YAHOO_API)
        WebExtractor.__init__(self, type=type, lang=lang, 
                              pages=pages, search=srch) 
        self.total_counts_cache = config.yahoo_limit
        self.total_counts = 0
        
    def _get_total_counts_from_cache(self):
        return utils.get_num_from_file(from_file = self.total_counts_cache)   
    
    def cache_total_counts(self):
        if self.total_counts > 0:
            utils.append_num_to_file(num = self.total_counts, 
                                          to_file = self.total_counts_cache)
    
    def __del__(self):
        """Before being destroyed, the system will register the number of counts used
        """
        self.cache_total_counts()
    
    def search(self):
        dom = self.srch.get_results()
        self.total_counts = self.total_counts + 1
        return self.srch.parse_results(dom)
    
    def get_count(self, results, cached=False):
        #return utils.random_int(0, 10000)
        return results.total_results_available
    
    def get_results(self, query, cached=False, start = START, pages = PAGES ):
        self.srch.query = query
        self.srch.start = start
        self.srch.results = pages
        return self.search()
    
    def get_proximity_query(self, list, pstr="*"):
        return WebExtractor.get_proximity_query(self, list, pstr)
    
    def get_alternative_proximity_query(self, list, pstr="*"):
        return WebExtractor.get_alternative_proximity_query(self, list, pstr)
      
    def get_snippets(self, results, cached=False):
        snippets = [(res['MimeType'], res.Url, res['Summary']) for res in results]
        return snippets
    
    def retrieve_summaries(self, query, start = START, pages = PAGES):
        results = self.get_results(query, start = start, pages = pages)
        snippets = self.get_snippets(results)
        summaries = [snippet[2].encode("utf8") for snippet in snippets]
        return summaries
        
        


class WebCounter():
    freq_file = "yahoo_db/freq.txt"
    cooc_file = "yahoo_db/cooc.txt"
    prox_file = "yahoo_db/prox.txt"
    
    def __init__(self, web_extractor=None, debug = config.DEBUG):
        if web_extractor:
            self.we = web_extractor
        else:
            self.we = YahooExtractor(lang=config.LANGUAGE)
        self.cooc_dict = {}
        self.freq_dict = {}
        self.prox_dict = {}
        self.total_counts = 0
        self.debug = debug
        self.we.debug = debug
        
        self._get_cache_from_files()
    
    def __del__(self):
        """
        called before destruction, putting all the calculated cache into files
        """
        self._put_cache_to_files()
    
            
    def _get_cache_from_files(self):
        self.cooc_dict = utils.get_dict_from_file(pattern = "(.+) - (\\d+)", 
                                                       from_file = self.cooc_file)
        self.freq_dict = utils.get_dict_from_file(pattern = "(.+) - (\\d+)", 
                                                       from_file = self.freq_file)
        self.prox_dict = utils.get_dict_from_file(pattern = "(.+) - (\\d+)", 
                                                       from_file = self.prox_file)
    
    def _put_cache_to_files(self):
        utils.put_dict_to_file(dict = self.freq_dict, to_file = self.freq_file)
        utils.put_dict_to_file(dict = self.cooc_dict, to_file = self.cooc_file)
        utils.put_dict_to_file(dict = self.prox_dict, to_file = self.prox_file)
        
    def list_to_hash(self, list):
        return ",".join(list)
    
    
    def cache_frequencies(self, words):
        for word in words:
            self.freq_dict[word] = self.count_frequency(word, cache=False)
    
    def cache_cooc(self, list):
        # store sorted
        sorted = list[:]
        sorted.sort()
        cooc = self.count_cooccurrence(sorted, cache=False)
        self.cooc_dict[self.list_to_hash(sorted)] = cooc
    
    def cache_proximity(self, list):
        """
        cache proximity for given list of terms
        """
        self.prox_dict[self.list_to_hash(list)] = self.count_proximity(list, cache=False)
    
    def cache_cooc_pairs(self, words):
        for word in words:
            for another_word in words:
                # TODO: the coocs might be slightly different, should all of them be taken
                # into consideration?
                if (not word == another_word):
                    self.cache_cooc([word, another_word])
    
    
    def extract_cache_value(self, dict, cache_func, list):
        hash = self.list_to_hash(list)
        if not hash in dict.keys():
             cache_func(list)
        count = dict[hash]
        return count
    
    def count_proximity(self, list, cache=False):
        prox_count = 0
        if cache:
            prox_count = self.extract_cache_value(self.prox_dict, 
                                                  self.cache_proximity, 
                                                  list)
            
        else:
            prox_query = self.we.get_alternative_proximity_query(list)
            prox_count = self.we.get_count(self.we.get_results(prox_query))
            
        return prox_count
    
    def count_frequency(self, term, context = [], cache=False):
        """
        caching only for requests without context
        """
        count = 0
        to_search = [term]
        if len(context) > 0:
            to_search.extend(context)
        if cache and len(context) == 0:
            count = self.extract_cache_value(self.freq_dict, 
                                             self.cache_frequencies, 
                                             to_search)
        else:
            query = self.we.get_cooc_query(to_search)
            if self.debug > 3:
                print "query %s" % query
            count = self.we.get_count(self.we.get_results(query))
            if self.debug > 0:
                print "Calculated frequency for %s in context %s - %d" % (term, 
                                                                          context,
                                                                          count)
        return count
    
    def count_query(self, query = ""):
        count = self.we.get_count(self.we.get_results(query))
        return count
                                  
    
    def count_cooccurrence(self, list, cache=False):
        count = 0
        sorted = list[:]
        sorted.sort()
        
        if cache:
            # in case of coocurrence the convention is to store the list sorted
            
            count = self.extract_cache_value(self.cooc_dict, 
                                             self.cache_cooc, 
                                             sorted)
        else:
            query = self.we.get_cooc_query(sorted)
            count = self.we.get_count(self.we.get_results(query))
            if self.debug:
                print "Calculated cooc for terms %s - %d" % (sorted, count)
        return count     
        
    def count_proximity_over_cooc(self, list, cache=False):
        """
        list - check proximity over cooccurrence for the given list of terms
        
        """
        prox = self.count_proximity(list, cache)
        cooc = self.count_cooccurrence(list, cache)
        result = utils.divide(prox, cooc)
        if self.debug:
            print "Calculated proximity count for terms %s - %0.5f (cooc - %d)" % (list, 
                                                                                  result, 
                                                                                  cooc)
        return result
    
    def count_cooc_and_freq(self, list, cache=False):
        """
        @return: a tuple with:
        1) the count for cooccurrence of the items in the list
        2) a list of frequencies for each one of the items
        """
        cooc = self.count_cooccurrence(list, cache)
        frequencies = []
        for term in list:
            frequencies.append(self.count_frequency(term, context = [], cache = cache))
        return (cooc, frequencies)
    
    def count_cooc_over_freq(self, list, cache=False):
        
        cooc, frequencies = self.count_cooc_and_freq(list, cache)
        return utils.count_num_over_denom(cooc,
                                               utils.sum(frequencies))
    
    def count_cooc_over_min_freq(self, list, cache=False):
        
       cooc, frequencies = self.count_cooc_and_freq(list, cache)
       return utils.divide(cooc, min(frequencies))
            
          
def test():
    
    ye = YahooExtractor(lang=config.LANGUAGE)
#    query = ye.get_proximity_query(['apple', 'pear'])
#    results = ye.get_results(query)
#    print ye.get_count(results)
#    
#    print ye.retrieve_summaries(query)
    
    wc = WebCounter(web_extractor = ye)
    
    print wc.count_frequency('intelligent', ['unintelligent', 'bright'],  cache = False)
    #print wc.count_proximity_over_cooc(['Monday', 'Tuesday'])
    #print wc.count_proximity_over_cooc(['Tuesday', 'Monday'])
    
    
if __name__ == "__main__":
    test()     
    
        
