from whoosh.qparser import QueryParser
import whoosh.index as index
import codecs

class Searcher:

    def search(self, query):
        ix = index.open_dir("indexdir")
        qp = QueryParser("title", schema=ix.schema)
        q = qp.parse(unicode(query))
        with ix.searcher() as s:
            results = s.search(q)
	    print "Number of results: ", len(results)
            for hit in results:
                #print(hit["title"])
                # Assume the "path" stored field contains a path to the original file
                with codecs.open(hit["path"], "r", "utf-8") as fileobj:
                    filecontents = fileobj.read()
                print hit.highlights("title", text=filecontents)
