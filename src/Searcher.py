# -*- coding: utf-8 -*-
from whoosh.qparser import QueryParser
import whoosh.index as index


class Searcher:

    def search(self, query):
        ix = index.open_dir("indexdir")
        #ix_reader = ix.reader()
        #results = ix_reader.field_length("title")
        #print results
        ##for rs in results:
            #print rs
        qp = QueryParser("title", schema=ix.schema)
        q = qp.parse(unicode(query))
        with ix.searcher() as s:
            results = s.search(q)
            for hit in results:
                print(hit["title"])
                # Assume the "path" stored field contains
                # a path to the original file
                with open(hit["path"]) as fileobj:
                    filecontents = fileobj.read()
                print(hit.highlights("content", text=filecontents))

            for rs in results:
                print "the title is:" + str(rs)