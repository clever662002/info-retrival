from whoosh.reading import IndexReader
from whoosh.searching import Searcher, Hit
from whoosh.qparser import MultifieldParser
import whoosh.index as index
import whoosh.scoring as score
import codecs

class Searcher:

    def __init__(self):
	self.ix = index.open_dir("indexdir")

    def search(self, query):
        fieldnames = ["title", "th", "h1", "h2", "h3", "h4", "h5",
                        "h6", "p", "blockquote", "td", "li", "label", "div",
                        "section"]
        qp = MultifieldParser(fieldnames, schema=self.ix.schema)
        q = qp.parse(unicode(query))
	
	# DEBUG: Print out contents of index.
#	reader = self.ix.reader()
#	terms = reader.all_terms()
#	for t in terms:
#		print t

	# Searcher object instantiated here.
        with self.ix.searcher() as s:
	    v = s.vector(0, "content")
	    for i in v.items_as("frequency"):
		print i
#            results = s.search(q, terms=True)
#	    # Display results for each Hit.
#	    for r in results:
#		for e in r.fields().keys():
#			print e, ":", r[e]
#		#print r.fields()['path'][54:]
#		print "***********************************"





