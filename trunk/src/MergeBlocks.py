import heapq
import os
from ast import literal_eval


class MergeBlocks:
    def _init_(self):
        pass

    def unmarshall(self, path, start_line):
        terms = dict()
        linenum = 0
        block_size = 1000
        input_file = open(path, "rb")
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
        #create a start_line list for each dictionary in the list
        #to remember the reading point
        start_line = list()
        path = 'D:/workspace/InfoRetrival/src/'
        # Initialize a list of blocks(each block is a heap queue)
        for filename in os.listdir(path):
            heap = []
            if filename.endswith('.s'):
                block = self.unmarshall(path + filename, 0)
                # push each item in the dictionary into the heap queue
                for item in block.items():
                    heapq.heappush(heap, item)
                start_line.append(len(heap))
                queueList.append(heap)
        # Compare the top element of each queue
        #and get the lowest top element from each queue and pop it
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
                #if find the key pop
                #that (key,posting) item out of the dictionary
                if(list(q[0])[0] == min_term):
                    temp_elt = heapq.heappop(q)
                    # merge all the popped out results
                    temp = list(temp_elt)
                    temp_list = list(temp[1])
                    postings.extend(x for x in temp_list if x not in postings)
                    # if the queue is all popped out,
                    #refill the queue by loading a new block
                    if len(q) == 0:
                        q_index = queueList.index(q)
                        print "The file needs to be refilled is :" + str(q_index)
                        startpoint = start_line[q_index]
                        block = self.unmarshall(path + 'temp' + str(q_index)  + '.s' , startpoint)
                        # push each item in the dictionary into the heap queue
                        for item in block.items():
                            heapq.heappush(q, item)
                        start_line[q_index] = startpoint + len(q)

                        # if the returned block is empty,
                        #it means u r done with that file,
                        #so remove the relevant queue from the queue list
                        if len(q) == 0:
                            queueList.remove(q)
            #after get the min_term and its postings, assemble them together
            result[min_term] = postings
            #after result dictionary is bigger than a block,
            #write it back to the final file
            if(len(result) > 1000):
                fin_output = open('final.t', 'ab')
                for key in result.keys():
                    fin_output.write(key + ":" + str(tuple(result[key])) + "\n")
                result.clear()
                fin_output.close()
        # to make sure after all queues are empty,
        #the last result is write into the file
        if result:
            fin_output = open('final.t', 'ab')
            for key in result.keys():
                fin_output.write(key + ":" + str(tuple(result[key])) + "\n")
            fin_output.close()