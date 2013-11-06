import sys
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
                    #associate posting lists in the same ordermai
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