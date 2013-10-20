'''
Created on 2013-10-16

@author: tina
'''
#!/usr/bin/python
import os
import string
import sys
from ast import literal_eval
import heapq
class Analyzer(object):
    '''
    for each input string, process it and extract tokens
    '''

    def __init__(self):
        pass
    
    def getstopwords(self):
        stopw_file = open('stopw.txt')
        stopw_file_string = stopw_file.read()
        stop_words =stopw_file_string.split(",")
        stop_list =[x.strip() for x in stop_words]
        return stop_list


    def tokenize(self,doc):
        stop_list = self.getstopwords()
        tokens = list()
        #remove capital letters, punctuation, newline and tab
        doc = doc.lower().translate(None,string.punctuation.join('\n\t'));
        #remove numbers
        doc = ''.join([i for i in doc if not i.isdigit()])
        #split tokens on spaces
        for token in doc.split(" "):
            if not token in stop_list:
                tokens.append(token)
        return tokens
    
class Parser:
    def parse(self,path):
        input_file = open(path).read()
        #create a list which will contain the documents
        collection = list()
        #Process the input file to extract document
        while 1:
            try:
                #extract document content
                i = input_file.index("<BODY>") + 6
                j = input_file.index("</BODY>")
                #Append the document to our list
                collection.append(input_file[i:j])
                #Move forward on the input
                input_file = input_file[j+7:]
            except:
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
        self.tempNum = 0
    def process(self, collection):
        """Extract tokens from a document """
        # parse into blocks
        memsize = 550000
        for doc in collection:
            doc_id = collection.index(doc)
            document_tokens = self.analyser.tokenize(doc)
            for token in document_tokens:
                posting_list = self.terms.get(token,[])
                if not doc_id in posting_list:
                    posting_list.append(doc_id)
                    self.terms[token] = posting_list
                # if the file size is reached or bigger than the memory size, parse into a block
                if(sys.getsizeof(self.terms) > memsize):
                    #sorted the keys
                    sorted_terms = self.terms.keys()
                    sorted_terms.sort()
                    #associate posting lists in the same order
                    sorted_postings = list()
                    for st in sorted_terms:
                        sorted_postings.append(self.terms[st])
                    # iterate through both lists, and save it to a string to be written to file
                    output = str()
                    for term,postings in zip(sorted_terms,sorted_postings):
                        output += term + ":" + str(tuple(postings)) + "\n"
                    #cut off the first empty key line
                    
                    #cut off the last "\n" to avoid an empty line
                    output = output[:-1]
                    #write it to a binary file
                    output_file = open("temp" + str(self.tempNum) + ".s", "wb")
                    output_file.write(output)
                    output_file.close()
                    #clear the 
                    self.terms.clear()
                    self.tempNum  = self.tempNum + 1    
    def get_index(self):
        return self.terms


class MergeBlocks:
    
    def _init_(self):
        pass
    
    def unmarshall(self,path,start_line):
        
        terms = dict()
        linenum = 0
        block_size = 1000
        input_file = open(path,"rb")
        while True:
            line = input_file.readline()
            linenum = linenum + 1
            if not line or (linenum - start_line) > block_size:
                break
            if linenum > start_line:
                temp = line.split(":")
                term = temp[0]
                postings = literal_eval(temp[1])
                terms[term] = postings
        input_file.close()
        return terms
    
    def mergeblock(self):
        queueList = list()
        #create a start_line list for each dictionary in the list to remember the reading point
        start_line = list() 
        path = 'D:/MyDocuments/workspace/InfoRetrival/src/'
        # Initialize a list of blocks(each block is a heap queue) 
        for filename in os.listdir(path):
            heap = []
            if filename.endswith('.s'):
                block = self.unmarshall(path + filename,0)
                # push each item in the dictionary into the heap queue
                for item in block.items():
                    heapq.heappush(heap,item)
                start_line.append(len(heap))
                queueList.append(heap)
                
                
                
        # Compare the top element of each queue and get the lowest top element from each queue and pop it
        result = dict()
        # remember the postings entries for report use
        while queueList:
            # get first queue top element
            temp_term = list(queueList[0][0])
            min_term = list(temp_term)[0]
            for q in queueList:
                key = list(q[0])[0]
                if min_term > key:
                    min_term = key
            # get the min_term posting lists and merge to a new posting list
            postings = list()
#            temp_list = list()
            for q in queueList:
                #if find the key pop that (key,posting) item out of the dictionary
                if(list(q[0])[0] == min_term):
                    temp_elt = heapq.heappop(q)
                    # merge all the popped out results
                    temp = list(temp_elt)
                    temp_list = list(temp[1])                   
                    postings.extend(x for x in temp_list if x not in postings)

                    # if the queue is all popped out, refill the queue by loading a new block 
                    if len(q) == 0 :
                        q_index = queueList.index(q)
                        print "The file needs to be refilled is :" + str(q_index)
                        startpoint = start_line[q_index]
                        block = self.unmarshall(path + 'temp' + str(q_index)  + '.s' , startpoint)
                        # push each item in the dictionary into the heap queue
                        for item in block.items():
                            heapq.heappush(q,item)
                        start_line[q_index] = startpoint + len(q)
                        
                        # if the returned block is empty, it means u r done with that file, so remove the relevant queue from the queue list
                        if len(q) == 0:
                            queueList.remove(q)
            #after get the min_term and its postings, assemble them together
            result[min_term] = postings
            #after result dictionary is bigger than a block, write it back to the final file
            if(len(result) > 1000):
                fin_output = open('final.t','ab')
                for key in result.keys():
                    fin_output.write(key + ":" + str(tuple(result[key])) + "\n")
                result.clear()
                fin_output.close()
        # to make sure after all queues are empty, the last result is write into the file 
        if result:
            fin_output = open('final.t','ab')
            for key in result.keys():
                fin_output.write(key + ":" + str(tuple(result[key])) + "\n")
            fin_output.close()
class IndexSearcher(object):
   
    def __init__(self, analyser):
        # Create a dictionary (hash table) which will contain the posting lists
        self.analyser = analyser
    
    def searchtokens(self,token):
        path = 'D:/MyDocuments/workspace/InfoRetrival/src/final.t'
        input_file = open(path,"rb") 
        terms = dict()      
        while True:
            line = input_file.readline()
            if not line:
                break
            temp = line.split(":")
            term = temp[0]
            if token == term:
                postings = literal_eval(temp[1])
                terms[term] = postings
                break
        input_file.close()
        return terms
        
    def or_query(self,query):
        docs = set()
        for token in self.analyser.tokenize(query):
            terms = self.searchtokens(token)
            if terms:
                if terms[token]:
                    postings = list(terms[token])
                    docs = docs.union(set(postings))
                else:
                    continue
            else:
                continue
        return docs

    def and_query(self,query):
        qtoken = self.analyser.tokenize(query)
        if self.searchtokens(qtoken[0]):
            docs = set(set(self.searchtokens(qtoken[0])[qtoken[0]]))
        else:
            docs = set()
        for token in qtoken:
            terms = self.searchtokens(token)
            if terms:
                if terms[token]:
                    postings = list(terms[token])
                    docs = docs.intersection(set(postings))
                else:
                    break
            else:
                break
        return docs
# main function
if __name__ == '__main__':
    collection = list()
    parser = Parser()
    analyser = Analyzer()
    index_writer = IndexWriter(analyser)
    merge = MergeBlocks()
    
#   args = sys.argv
#   path = args[1]
    '''
    path = 'D:/MyDocuments/workspace/InfoRetrival/reuters21578/'
    # index the Reuters dataset
    for filename in os.listdir(path):
        if filename.endswith('.sgm'):
            print filename
            collection = parser.parse(path + filename)
            index_writer.process(collection)
    merge.mergeblock() 
    '''
    insearch = IndexSearcher(analyser)
    query = "apple"
    result = insearch.and_query(query)
    print 'The query result is: '
    for r in result:
        print r,
    

