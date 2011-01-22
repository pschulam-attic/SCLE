'''
Created on Jul 22, 2010

@author: Peter F. Schulam
'''

class TextReader():
    '''
    A class that is instantiated with a text file. The
    class provides an API for reading file.
    '''

#===============================================================================
# Non-public methods
#===============================================================================

    def __init__(self, filename):
        '''
        @param filename: name of the file that the Reader will operate on.
        '''
        self._file_handle = open(filename, 'r')
        self._next_line = ''
        self._chars_in_current_line = 0
        self._empty = False
        self._load_next_line()
        
    def __del__(self):
        self._file_handle.close()
        
    def _load_next_line(self):
        '''
        Loads the next line of the piece of text and updates relevant information
        '''
        self._next_line = self._file_handle.readline().lstrip().replace('\n', ' ')
        self._chars_in_current_line = len(self._next_line)
        if self._next_line == '':
            self._empty = True
        
    def _get_next_char(self):
        '''
        Gets the next char from the file
        '''
        c = self._next_line[0]
        self._next_line = self._next_line[1:]
        self._chars_in_current_line -= 1
        if (self._chars_in_current_line == 0):
            self._load_next_line()
        return c
    
    def _put_char(self, c):
        '''
        Puts the character 'c' back on the front of the text.
        '''
        self._next_line = c + self._next_line
        self._chars_in_current_line += 1
        
    def _get_next_token(self):
        '''
        Gets the next space separated token from the file.
        '''
        token = []
        c = self._get_next_char()
        
        while c.isspace():
            c = self._get_next_char()
        while not c.isspace():
            token.append(c)
            c = self._get_next_char()
        
        self._put_char(c)
        return ''.join(token)
    
    def _get_next_sentence(self, format='string'):
        '''
        Gets the next sentence from the file.
        
        @param format: returns the sentence as a string if 'string' and as a list containing
        the constituent words if 'list'.
        '''
        sentence = []
        in_sentence = True
        
        while in_sentence:
            word = self._get_next_token()
            if word.endswith(('.', '!', '?')):
                in_sentence = False
            sentence.append(word)
        
        if format == 'string':
            return ' '.join(sentence)
        else:
            return sentence

#===============================================================================
# Public methods
#===============================================================================

    def get_char(self, num_chars=1):
        '''
        Gets 'num_chars' characters from the file. 1 character is returned by default.
        If the text has been exhausted the empty string is returned.
        
        @param num_chars: number of characters to return.
        '''
        if self._empty:
            return ''
        
        return_list = []
        
        for _ in range(num_chars):
            return_list.append(self._get_next_char())
        
        if num_chars == 1:
            return return_list[0]
        else:
            return return_list

    def get_word(self, num_words=1):
        '''
        Gets 'num_words' words from the text. If 'num_words' is not specified, 1 word is
        returned by default. If the text has been exhausted the empty string is returned.
        
        @param num_words: number of words to return
        '''
        if self._empty:
            return ''
        
        return_list = []
        
        for _ in range(num_words):
            return_list.append(self._get_next_token().rstrip('.,!?'))
            
        if num_words == 1:
            return return_list[0]
        else:
            return return_list
    
    def get_sentence(self, num_sentences=1, format='string'):
        '''
        Gets the next 'num_sentences' sentences from the text and returns them in a list.
        The caller can specify the format of each sentence by passing the 'format' argument as
        'string' or 'list'. If the text has been exhausted the empty string is returned.
        
        @param num_sentences: number of sentences to read
        @param format: specifies whether each sentence should be a full string or a list of words
        '''
        if self._empty:
            return ''
        
        return_list = []
        
        for _ in range(num_sentences):
            return_list.append(self._get_next_sentence(format))
            
        if num_sentences == 1:
            return return_list[0]
        else:
            return return_list

