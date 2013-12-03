import whoosh.index as index
from whoosh.qparser import MultifieldParser

class Kmean:

    def __init__(self):
		pass

    def kmeans(self, query, index):
        # creating document collection
        # the collection is like ((doc1: (term1: 4),(term2: 5)),(doc2(...)),...)
        doc_collection = dict()
        with index.searcher() as s:
            # Returns a generator of the document numbers for all documents
            for i in s.document_numbers():
                doc_item = list()
                v = s.vector(i, "content")
                for term_item in v.items_as("frequency"):
                    doc_item.append(term_item)
                doc_collection[i] = doc_item

            #for i in doc_collection.items():
                #print i

        # Creating document collection only with the query terms' frequency
        doc_query_collection = dict()

        # Parsing the query
        # Returns a set of all terms in this query tree.
        for q_item in query.all_terms(phrases=True):
            #first_elts = [x[1] for x in doc_collection.items()]
            for doc in doc_collection:
                print doc
            #for doc in doc_collection.items():
                ## get the value of the key as q_item,
                ## if it does not exist, return 0
                #if q_item in doc[0]:
                    #print q_item
					##tf = doc.values()[1]
					##doc_query_collection[doc] = tf

        for i in doc_query_collection.items():
            print i

#        #Create clusters collection
#        #(cluster1:((center:query_term1:4)(d1:(...),...),cluster2(),cluster3())
#        cluster = dict()
#        #Randomely Pick three seeds from doc_query_collection
#        cluster['c1'] = doc_query_collection[0]
#        cluster['c2'] = doc_query_collection[1]
#        cluster['c3'] = doc_query_collection[2]
#        #set the center elements as those three documents as a start
#        cluster['c1']['center'] = cluster['c1'][0]
#        cluster['c2']['center'] = cluster['c2'][0]
#        cluster['c3']['center'] = cluster['c3'][0]
#        #iterate 10 times:
#        for i in range[0, 10]:
#            # loop through all documents in doc_query_collection
#            # to compare the distance and calculate the center
#            for dq in doc_query_collection:
#                #build distance dict((c1:d1), (c2:d2), (c3:d3))
#                distance = dict()
#                for cl in cluster:
#                    d = 0
#                    for qitem in dq.keys():
#                        #(dtf-ctf)^2
#                        d +=(dq[qitem] - cl['center'][qitem]) * (dq[qitem]-cluster['c1']['center'][qitem])
#                    distance[cl] = d
#                # move uncliassified document dq
#                #into the cluster with smallest distance
#                for ditem in distance:
#                    if ditem.value == min(distance.values()):
#                        cl_new = ditem.key()
#                #check the new doc whether is classifled
#                for cl in cluster:
#                    # if the document is in one of the cluster, remove it
#                    if cl[dq]:
#                        del cl[dq]
#                    # add the document to the new cluster
#                    cl_new[dq] = dq
#                    #update the center element of cl_new:
#                    for qt in cl_new.values():
#                        total_f = 0
#                        total_f += qt[1]
#                        # since it adds the center into
#                        # it needs to subtract it from total_f
#                        total_f = total_f - cl_new["center"][qt[0]]
#                        # len - -1 because the total lengh
#                        # needs to subtract center one
#                        center_new = total_f / (len(cl_new) - 1)
#                        # update center value:
#                        cl_new["center"][qt[0]] = center_new
#        return cluster






















