'''
Created on 2013-10-16

@author: tina
'''

class IndexWriter(object):
    '''
    for each document, clean it, tokenize it and store the terms in posting lists
    '''


    def __init__(self, analyser):
        # Create a dictionary (hash table) which will contain the posting lists
        self.terms = dict()
        self.analyser = analyser
    def process(self, collection):
        """Extract tokens from a document """
        for doc_id in collection:
            document_tokens = self.analyser.tokenize(collection[doc_id])
            for token in document_tokens:
                posting_list = self.terms.get(token, [])
                if not doc_id in posting_list:
                    posting_list.append(doc_id)
                    self.terms[token] = posting_list
    def get_index(self):
        return self.terms