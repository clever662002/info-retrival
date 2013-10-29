from ast import literal_eval
class IndexSearcher(object):
   
    def __init__(self, analyser):
        # Create a dictionary (hash table) which will contain the posting lists
        self.analyser = analyser
    
    def searchtokens(self,token):
        path = 'D:/workspace/InfoRetrival/src/final.t'
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