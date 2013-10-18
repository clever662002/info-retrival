'''
Created on 2013-10-17

@author: tina
'''
from ast import literal_eval
import heapq
import csv
foo = dict()
foo = {'a':'1,2,3', 'b':'20,','c':'3,','e':'1,'}
postings = list()
temp_list = list()


heap=[]
# add some values to the heap
for t in foo.items():
    heapq.heappush(heap,t)


             
'''
for value in [20, 10, 30, 50, 40]:
    heapq.heappush(heap, value)
'''
# pop them off, in order
while heap:
    result = heapq.heappop(heap)
    temp = list(result)
    temp_list = list(temp[1])
    postings.extend(x for x in temp_list if x not in postings and x != ',')
for p in postings:
    print postings