'''
Created on 2013-10-16

@author: tina
'''
from Parser import Parser
from Indexing import Indexing
from Searcher import Searcher
import whoosh.index as index

# main function
if __name__ == '__main__':
    collection = dict()
    parser = Parser()
    indexer = Indexing()
    path = "/home/katherine/COMP479/info-retrieval/trunk/src/test/"
    # Parse the documents
    collection = parser.parse(path)
    # Index the documents
    indexer.process(collection)
    print "Finish Indexing."

#    # Creater Searcher object.
    searcher = Searcher()

#    # Query the index
    query = "teaching"
    searcher.search(query)
