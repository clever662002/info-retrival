'''
Created on 2013-10-16

@author: tina
'''
import string

class Analyzer(object):
    '''
    for each input string, process it and extract tokens
    '''

    def __init__(self):
        pass
    def tokenize(self,doc):
        tokens = list()
        #remove capital letters, punctuation, newline and tab
        doc = doc.lower().translate(None,string.punctuation.join('\n\t'));
        #slit tokens on spaces
        for token in doc.split(" "):
            tokens.append(token)
        return tokens