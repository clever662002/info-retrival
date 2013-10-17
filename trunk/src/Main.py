'''
Created on 2013-10-16

@author: tina
'''
#!/usr/bin/python
#import IndexSearcher
import os
import string
import sys

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
        #split tokens on spaces
        for token in doc.split(" "):
            tokens.append(token)
        return tokens
    
class Parser:
    def parse(self,path):
        input_file = open(path).read()
        #create a list which will contain the documents
#        collection = dict()
        collection = list()
        #Process the input file to extract document
        while 1:
            try:
                #extract document date as its key
#                i = input_file.index("<DATE>") + 6
#                j = input_file.index("</DATE>")
#                filename = path + "." + input_file[i:j]
                #extract document content
                i = input_file.index("<BODY>") + 6
                j = input_file.index("</BODY>")
                #Append the document to our list
                collection.append(input_file[i:j])
                #Move forward on the input
                input_file = input_file[j+7:]
            except:
                print 'return from parsing'
            # if input_file.index("<BODY>") fails, we will end up here
            # meaning the whole collection has been processed
                break
        return collection
    
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
        limit = 3000
        tempNum = 0
        for doc in collection:
            doc_id = collection.index(doc)
            document_tokens = self.analyser.tokenize(doc)
            for token in document_tokens:
                posting_list = self.terms.get(token, [])
                if not doc_id in posting_list:
                    posting_list.append(doc_id)
                    self.terms[token] = posting_list
                if(sys.getsizeof(self.terms) > limit):
                    for term in self.terms:
                        output_file = open("temp" + str(tempNum) + ".txt", "w")
                        docids = ', '.join(map(str,self.terms[token]))
                        output_file.write(term + docids)
                    output_file.close()
                    self.terms = []
                    tempNum  = tempNum + 1                   
                
    def get_index(self):
        return self.terms

if __name__ == '__main__':
    collection = list()
    parser = Parser()
    analyser = Analyzer()
    index_writer = IndexWriter(analyser)
    
#   args = sys.argv
#   path = args[1]
    path = 'D:/workspace/InfoRetrieval/reuters21578/'
    # index the Reuters dataset
    for filename in os.listdir(path):
        if filename.endswith('.sgm'):
            collection = parser.parse(path + filename)
            index_writer.process(collection)
             
#   terms = index_writer.get_index()
#   index_reader = IndexSearcher(analyser,terms)
#   print len(index_reader.and_query("In view of the lower"))


