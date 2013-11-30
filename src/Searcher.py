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
            results = s.search(q, terms=True)
	    for r in results:
		print r.fields()
	    print "Number of results:", len(results)
	    # Get a random hit object from results and convert it to dict with .fields() call
#	    r = random.choice(results).fields()
#	    print r
#	    for hit in results:
#		print (hit.highlights("content")), "\n**********************************\n"






