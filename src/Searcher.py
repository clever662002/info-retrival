import whoosh.index as index
from whoosh.qparser import MultifieldParser
#from whoosh.qparser import QueryParser
import codecs


class Searcher:

    def search(self, query):
        fieldnames = ["title", "th", "h1", "h2", "h3", "h4", "h5",
                        "h6", "p", "blockquote", "td", "li", "label", "div",
                        "section"]
        ix = index.open_dir("indexdir")
        qp = MultifieldParser(fieldnames, schema=ix.schema)
        q = qp.parse(unicode(query))
        with ix.searcher() as s:
            results = s.search(q)
            print "Number of results: ", len(results)
            for hit in results:
                #print(hit["title"])
                # Assume the "path" stored field
                #contains a path to the original file
                with codecs.open(hit["path"], "r", "utf-8") as fileobj:
                    filecontents = fileobj.read()
                print hit.highlights("title", text=filecontents)
