'''
Created on 2013-10-16

@author: tina
'''
#!/usr/bin/python
#import os
#import math
#from Analyzer import Analyzer
#from IndexWriter import IndexWriter
#from IndexSearcher import IndexSearcher
#from MergeBlocks import MergeBlocks
# term frequency ranking
from Parser import Parser
from Indexing import Indexing
from Searcher import Searcher
#from whoosh.qparser import QueryParser
import whoosh.index as index


# main function
if __name__ == '__main__':
    #collection = list()
    #parser = Parser()
    #indexer = Indexing()
    searcher = Searcher()
    #path = "/home/tina/projects/test/"
    ##path = "/home/katherine/COMP479/info-retrieval/trunk/src/test/"
    ##Parse the documents
    #collection = parser.parse(path)
    ##Index the documents
    #indexer.process(collection)
    #print "Finish Indexing"
    ix = index.open_dir("indexdir")
    ix_reader = ix.reader()
    #results = ix_reader.all_terms()
    results = ix_reader.frequency("title", "concordia")
    print results
    #for rs in results:
        #print rs
    # Query the index
    query = "canada"
    searcher.search(query)

'''
def tf_rank(indexs, qterm):
    # score[doc] is the total score of a doc
    #which contains total frequencies of all terms
    score = dict()
    for qt in qterm:
        #each term's posting_list is like ('d1':tf,'d2':tf)
        posting_list = indexs.get(qt, {})
        for doc in posting_list.keys():
            #if a document does not exist yet, add it as a key of score,
            # and its value as an initializer of term frequency
            if not doc in score:
                score[doc] = posting_list[doc]
            # if a document already exists, accumulate its term frequencies.
            else:
                score[doc] = score[doc] + posting_list[doc]
    ranked_doc = sorted(score.items(), key=lambda x: x[1], reverse=True)
    print'ranking score for tf'
    for rd in ranked_doc[:10]:
        print rd[1]

    return ranked_doc


# okapi ranking
def okapi_rank(indexs, qterm, total_doc, k, doc_len, avgdl):
    #create a idf dictionary for each query term as key
    idf = dict()
    #create a score dictionary for each founded documents and rank them
    score = dict()
    for qt in qterm:
        posting_list = indexs.get(qt, {})
        #calculate the idf of each query term
        idf[qt] = math.log10((total_doc - len(posting_list) + 0.5)
                             / (len(posting_list) + 0.5))
        # calculate each doc's score
        #for doc in posting_list.keys():
            if not doc in score:
                score[doc] = idf[qt] * (((posting_list[doc]) * (k + 1))
                 /(posting_list[doc] + k * (1 - 0.75 + 0.75 * (doc_len[doc]
                  / avgdl))))
            else:
                score[doc] = score[doc] + idf[qt] *
                (((posting_list[doc]) * (k + 1)) /(posting_list[doc] + k *
                (1 - 0.75 + 0.75 * (doc_len[doc] / avgdl))))
    ranked_doc = sorted(score.items(), key=lambda x: x[1], reverse=True)
    print'ranking score for okapi'
    for rd in ranked_doc[:10]:
        print rd[1]
    return ranked_doc


# main function
if __name__ == '__main__':
    collection = list()
    parser = Parser()
    analyser = Analyzer()
    index_writer = IndexWriter(analyser)
    #merge = MergeBlocks()

    print'Initializing IndexWriter'
    path = 'D:/MyDocuments/workspace/InfoRetrival/reuters21578/'
    #store all searched documents
    #and its length is a total number of documents(total_doc)
    allcollection = list()
    #stores doc as its key
    #and total number of tokens for each document as its value
    doc_len = dict()
    # loop through all reuters
    print'Found index on disk'
    for filename in os.listdir(path):
        if filename.endswith('.sgm'):
            print 'Processing collection ' + filename
            collection = parser.parse(path + filename)
            #after the parser parses one .sgm to a collection,
            #add it to all collection for storing to a files
            allcollection.extend(collection)
            #tokenize each collection
            index_writer.process(collection)
            indexs = index_writer.get_index()
            doc_len = index_writer.get_doc_len()
    #number of documents
    total_doc = len(allcollection)
    print 'total number of documents in the collection is ' + str(total_doc)
    #total numbers of tokens in all documents
    total_token = sum(doc_len.values())
    print 'total number of tokens is ' + str(total_token)
    #average document length
    avgdl = total_token / total_doc
    print 'tokens per doc on average (total_token/total_doc) is ' + str(avgdl)
    print 'Inverted index is ready to use'
    print '***********************************************************'
    while True:
        print 'Query types:'
        print '1.Okapi BM25(default)'
        print '2.Sorted by term Frequency'
        print 'q.Exit'
        option = raw_input("Select a query type as above(1 or 2 or q):")
        if  option == 'q':
            print 'The program Terminate.'
            break
        elif option == str(2):
            query = raw_input("Enter a query:")
            qterm = analyser.tokenize(query)
            ranked_doc = tf_rank(indexs, qterm)
            for rd in ranked_doc[:5]:
                print rd[0]
                print '**************************************************'
        else:
            k = raw_input('Enter of k(default = 1.2):')
            if k:
                k = int(k)
            else:
                k = 1.2
            query = raw_input("Enter a query:")
            qterm = analyser.tokenize(query)
            ranked_doc = okapi_rank(indexs, qterm, total_doc, k, doc_len, avgdl)
            for rd in ranked_doc[:5]:
                print rd[0]
                print '**************************************************'
'''
'''
    #3 queries
    queries = list()
    queries.append('Democrats welfare and healthcare reform policies')
    queries.append('Drug company bankruptcies')
    queries.append('Dow jones great depression')

    for q in queries:
        qterm = analyser.tokenize(q)
        ranked_doc =okapi_rank(indexs,qterm,total_doc,k,doc_len, avgdl)

    for doc in ranked_doc[:5]:
        print doc
        print "******************************************************"

    #store all collection to a file
    all_doc = open("all_doc.d",'ab')
    for c in allcollection:
        all_doc.write(str(c) + '\n')
    all_doc.close()
    print 'finish writing files'
'''

'''
    merge.mergeblock()
    insearch = IndexSearcher(analyser)
    query = " bahia showers"
    result = insearch.or_query(query)
    print 'The query result is: '
    for r in result:
        print r,
'''

