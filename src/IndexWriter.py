'''
Created on 2013-10-16

@author: tina
'''
import sys

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
        # parse into blocks
        limit = 30000
        tempNum = 0
        for doc_id in collection:
            document_tokens = self.analyser.tokenize(collection[doc_id])
            
            for token in document_tokens:
                posting_list = self.terms.get(token, [])
                if not doc_id in posting_list:
                    posting_list.append(doc_id)
                    self.terms[token] = posting_list
                if(sys.getsizeof(self.terms) > limit):
                    for term in self.terms:
                        output_file = open("temp" + str(tempNum) + ".txt", "w")
                        output_file.write(term, self.terms[token])
                    output_file.close()
                    self.terms = []
                    tempNum  = tempNum + 1                   
                
    def get_index(self):
        return self.terms