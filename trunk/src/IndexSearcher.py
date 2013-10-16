'''
Created on 2013-10-16

@author: tina
'''

class IndexSearcher(object):
    '''
    search over stored index
    '''


    def __init__(self,analyser,term_index):
        self.analyser = analyser
        self.terms = term_index
    def or_query(self,query):
        docs = set()
        for token in self.analyser.tokenize(query):
            if self.terms.has_key(token):
                docs = docs.union(self.terms[token])
        return docs
        