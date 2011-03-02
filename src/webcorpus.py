'''
Created on Mar 2, 2011

@author: pschulam

NOTE: Much of the functionality is borrowed from code
written by Vera Sheinman.
'''

from yahoo.search.web import WebSearch

PAGES = 10
START = 1
YAHOO_API = "Peter.Schulam.Key"

class WebCorpus(object):
    '''
    Builds a corpus from Yahoo snippets given several
    keywords. 
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.s = WebSearch(YAHOO_API)
        self.total_counts = 0
        
    def search(self):
        dom = self.s.get_results()
        self.total_counts = self.total_counts + 1
        return self.s.parse_results(dom)
    
    def get_results(self, query, start=START, pages=PAGES):
        self.s.query = query
        self.s.start = start
        self.s.results = pages
        return self.search()

    def get_count(self, results):
        return results.total_results_available

    def get_snippets(self, results):
        snippets = [(res['MimeType'], res.Url, res['Summary']) for res in results]
        return snippets
    
    def get_summaries(self, query, start=START, pages=PAGES):
        results = self.get_results(query, start=start, pages=pages)
        snippets = get_snippets(results)
        summaries = [snippets[2] for snippet in snippets]
        return summaries
    
    
        
        
        