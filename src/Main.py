'''
Created on 2013-10-16

@author: tina
'''
#!/usr/bin/python
import os
from IndexSearcher import IndexSearcher
from Analyzer import Analyzer
from Parser import Parser
from IndexWriter import IndexWriter
from MergeBlocks import MergeBlocks

# main function
if __name__ == '__main__':
    collection = list()
    parser = Parser()
    analyser = Analyzer()
    index_writer = IndexWriter(analyser)
    merge = MergeBlocks()
    
#   args = sys.argv
#   path = args[1]
    while True:
        print 'Query types:'
        print '1.Okapi BM25(default)'
        print '2.Sorted by term Frequency'
        print 'q.Exit'
        qt = raw_input("Select a query type as above(1 or 2 or q):")
        if qt == 'q':
            print 'The program Terminate.'
            break
        else:
            print 'HAHa I choose option:' + qt
            k = 1.2
            k = raw_input("Enter of k(default= 1.2)")
            print 'Test k =' + str(k)
            
    #store all documents from all .sgm files
    allcollection = list()
    path = 'D:/workspace/InfoRetrival/reuters21578/'
    # index the Reuters dataset
    for filename in os.listdir(path):
        if filename.endswith('.sgm'):
            print filename
            collection = parser.parse(path + filename)
            #after the parser parses one .sgm to a collection, add it to all collection for storing to a files
            allcollection.extend(collection)
            #tokenize each collection
            index_writer.process(collection)
    #store allcollection to a file
    all_doc = open("all_doc.d",'ab')
    for c in allcollection:
        all_doc.write(str(c) + '\n')
    all_doc.close()
    print 'finish writing files'
    '''
    merge.mergeblock() 
    insearch = IndexSearcher(analyser)
    query = " bahia showers"
    result = insearch.or_query(query)
    print 'The query result is: '
    for r in result:
        print r,
    '''

