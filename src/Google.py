#/***************************************************************************
# *   Copyright (C) 2008 by matt@blackcodeseo.com                           *
# *   http://blackcodeseo.com/                                              *
# *
# *   Modications by: Andy Pavlo, Brown University                          *
# *   http://www.cs.brown.edu/~pavlo/                                       *
# *                                                                         *
# *   Permission is hereby granted, free of charge, to any person obtaining *
# *   a copy of this software and associated documentation files (the       *
# *   "Software"), to deal in the Software without restriction, including   *
# *   without limitation the rights to use, copy, modify, merge, publish,   *
# *   distribute, sublicense, and/or sell copies of the Software, and to    *
# *   permit persons to whom the Software is furnished to do so, subject to *
# *   the following conditions:                                             *
# *                                                                         *
# *   The above copyright notice and this permission notice shall be        *
# *   included in all copies or substantial portions of the Software.       *
# *                                                                         *
# *   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,       *
# *   EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF    *
# *   MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.*
# *   IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR     *
# *   OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, *
# *   ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR *
# *   OTHER DEALINGS IN THE SOFTWARE.                                       *
# ***************************************************************************/

from BeautifulSoup import BeautifulSoup, SoupStrainer
import mechanize
import urllib
import random

class Google():
    
    def __init__(self, **kwargs):
        self.setTitle(kwargs.get('title',None))
        self.setUrl(kwargs.get('url',None))
        self.setDescription(kwargs.get('description',None))
        
    def title(self):
        return self._title
    def setTitle(self, value):
        self._title = value
        
    def url(self):
        return self._url
    def setUrl(self, value):
        self._url = value
        
    def description(self):
        return self._description
    def setDescription(self, value):
        self._description = value

def getNextPage(data):
   links = SoupStrainer('a')
   href = filter(lambda tag: str(tag).count('Next') > 0, [tag for tag in BeautifulSoup(data, parseOnlyThese=links)])
   if href:
      href = str(href[-1])
      href = href[href.find('''"''') + 1:]
      href = href[:href.find('''"''')]
      return '%s%s' % ('http://www.google.com', href)
   else:
      return None
        
def getPageData(data):
    googles = []
    soup = BeautifulSoup(data)
    tags = soup('li')
    for tag in tags:
        title = ''.join([e for e in BeautifulSoup(str(tag('h3')[0])).recursiveChildGenerator() if isinstance(e,unicode)])
        url = str(tag('a')[0])
        url = url[url.find('''"''') + 1:]
        url = url[:url.find('''"''')]
        description = str(tag('div')[0])
        description = ''.join([e for e in BeautifulSoup(description[:description.find('<cite>')]).recursiveChildGenerator() if isinstance(e,unicode)])
        googles.append(Google(title=title, url=url, description=description))
    return googles

def generateUserAgent():
   ## Browser Type
   browsers = [ 'Mozilla/%.1f' % random.choice([4, 5, 6]),
                'Mozilla/%.1f' % random.choice([4, 5, 6]),
                'Opera/9.%d' % random.randint(0, 30) ]

   ## Browser Attributes
   attributes = [ ]
   attributes.append(random.choice([ 'textmode', 'compatible' ]))
   attributes.append(random.choice([ 'Intel Mac OS X 10.%d' % random.randint(1, 5), \
                                     'FreeBSD 6.%d-RELEASE i386' % random.randint(0, 4), \
                                     'Windows NT 5.%d' % random.randint(0, 2), \
                                     'Linux 2.6.%d i686' % random.randint(0, 30), \
                                   ]))
   if random.randint(0, 3) == 0: attributes.append(random.choice(['en', 'en-US', 'en-GB']))

   ## Put it all together
   ## This isn't perfect, but it's good enough
   return ('%s (%s)' %  (random.choice(browsers), '; '.join(attributes)))

def search(keywords, results=10):
    useragent = generateUserAgent()
    googles = []
    br = mechanize.Browser()
    br.addheaders = [("User-agent", useragent), 
                     ("HTTP_CONNECTION", "keep-alive"), 
                     ("HTTP_KEEP_ALIVE", "300"), 
                     ("HTTP_ACCEPT", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"),
                     ("HTTP_ACCEPT_CHARSET", "ISO-8859-1,utf-8;q=0.7,*;q=0.7"), 
                     ("HTTP_ACCEPT_ENCODING", "gzip,deflate"), 
                     ("HTTP_ACCEPT_LANGUAGE", "en-us,en;q=0.5"), 
                     ("HTTP_USER_AGENT", useragent)]
    br.set_handle_robots(False)
    br.open("http://www.google.com/search?client=firefox-a&rls=org.mozilla:en-US:official&" + \
             urllib.urlencode({"q": keywords, "num": results}))
    html = br.response().read()
    googles += getPageData(html)
    nextPage = getNextPage(html)
    while nextPage:
        br.open(nextPage)
        html = br.response().read()
        googles += getPageData(html)
        if len(googles) >= results:
            break
        nextPage = getNextPage(html)
    return len(googles)
    #if results > len(googles):
    #    results = len(googles)
    #return googles[:results]
