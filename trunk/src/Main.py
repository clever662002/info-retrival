'''
Created on 2013-10-16

@author: tina
'''
import Parser
import Analyzer
import IndexWriter
import IndexSearcher
import os
import sys

if __name__ == '__main__':
    collection = dict()
    parser = Parser()
    analyser = Analyzer()
    index_writer = IndexWriter(analyser)
    
    args = sys.argv
    path = args[1]
    # index the Reuters dataset
    for filename in os.listdir(path):
        if filename.endswith(".sgm"):
            collection = parser.parse(path + filename)
            index_writer.process(collection)
             
    terms = index_writer.get_index()
    index_reader = IndexSearcher(analyser,terms)
    print len(index_reader.and_query("In view of the lower"))