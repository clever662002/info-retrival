'''
Created on 2013-10-16

@author: tina
'''
#!/usr/bin/python
import os
import math
#from IndexSearcher import IndexSearcher
from Analyzer import Analyzer
from Parser import Parser
from IndexWriter import IndexWriter
#from MergeBlocks import MergeBlocks

    
def tf_rank(indexs,qterm):
    # score[doc] is the total score of a doc which contains total frequencies of all terms
    score = dict()
    for qt in qterm:
        #each term's posting_list is like ('d1':tf,'d2':tf)
        posting_list = indexs.get(qt,{})
        for doc in posting_list.keys():
            #if a document does not exist yet, add it as a key of score, and its value as an initializer of term frequency
            if not doc in score:
                score[doc] = posting_list[doc]
            # if a document already exists, accumulate its term frequencies.
            else:
                score[doc] = score[doc] + posting_list[doc]
    ranked_doc = sorted(score, key=lambda x:x[1], reverse=True)
    print "ranked doc is a type of :" +  str(type(ranked_doc))
    return ranked_doc
    
def okapi_rank(indexs,qterm,total_doc, k, doc_len, avgdl):
    #create a idf dictionary for each query term as key
    idf = dict()
    #create a score dictionary for each founded documents and rank them
    score = dict()    
    for qt in qterm:
        posting_list = indexs.get(qt,{})
        #calculate the idf of each query term
        idf[qt] = math.log10((total_doc - len(posting_list) + 0.5) / (len(posting_list) + 0.5))
        # calculate each doc's score
        for doc in posting_list.keys():
            if not doc in score:
                score[doc] = idf[qt] * (((posting_list[doc]) * (k + 1)) /(posting_list[doc] + k * (1 - 0.75 + 0.75 * (doc_len[doc] / avgdl))))
            else:
                score[doc] = score[doc] + idf[qt] * (((posting_list[doc]) * (k + 1)) /(posting_list[doc] + k * (1 - 0.75 + 0.75 * (doc_len[doc] / avgdl))))    
    for s in score.items():
        print s[1];
    ranked_doc = sorted(score, key=lambda x:x[1],reverse=True)     
    return ranked_doc                                                         
                                        

# main function
if __name__ == '__main__':
    collection = list()
    parser = Parser()
    analyser = Analyzer()
    index_writer = IndexWriter(analyser)
#    merge = MergeBlocks()

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
            print 'Haha I choose option:' + qt
            k = 1.2
            k = raw_input("Enter of k(default= 1.2)")
            print 'Test k =' + str(k)
            
    #store all documents from all .sgm files, and its length is total number of documents
    allcollection = list()
    path = 'D:/workspace/InfoRetrival/reuters21578/'
    # index the Reuters dataset
    doc_len = dict()
    for filename in os.listdir(path):
        if filename.endswith('.sgm'):
            print filename
            collection = parser.parse(path + filename)
            #after the parser parses one .sgm to a collection, add it to all collection for storing to a files
            allcollection.extend(collection)
            #tokenize each collection
            index_writer.process(collection)
            indexs = index_writer.get_index()
            doc_len = index_writer.get_doc_len()
            
            
    total_doc =len(allcollection)
    total_token = sum(doc_len.values())
    print 'total token is ' + str(total_token)
    #average document length
    avgdl = total_token/total_doc
    k = 1.2
    print avgdl
    
        
        
    #3 queries
    queries = list()
#    queries.append('Democrats welfare and healthcare reform policies')
#    queries.append('Drug company bankruptcies')
    queries.append('Dow jones great depression')
    
    for q in queries:
        qterm = analyser.tokenize(q)
        ranked_doc =okapi_rank(indexs,qterm,total_doc,k,doc_len, avgdl)
        '''
        for doc in ranked_doc:
            print doc
            print "**************************"
       '''

    #store all collection to a file
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

