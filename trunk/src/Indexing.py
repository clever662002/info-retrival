# -*- coding: utf-8 -*-
import os
from whoosh import index
from whoosh.fields import *
from bs4 import BeautifulSoup

class Indexing:

    def __init__(self):
        self.schema = Schema(title=TEXT(field_boost=5.0),
                        th=TEXT(field_boost=4.0),
                        h1=TEXT(field_boost=4.0),
                        h2=TEXT(field_boost=3.0),
                        p=TEXT(field_boost=3.0),
                        blockquote=TEXT(field_boost=3.0),
                        td=TEXT(field_boost=3.0),
                        li=TEXT(field_boost=3.0),
                        h3=TEXT(field_boost=2.0),
                        label=TEXT(field_boost=2.0),
                        span=TEXT(field_boost=2.0),
                        h4=TEXT(field_boost=2.0),
                        h5=TEXT(field_boost=2.0),
                        h6=TEXT(field_boost=2.0),
                        div=TEXT,
                        section=TEXT)

    def process(self, collection):
        if not os.path.exists("indexdir"):
            os.mkdir("indexdir")
        self.ix = index.create_in("indexdir", self.schema)
        self.ix = index.open_dir("indexdir")
        writer = self.ix.writer()

        for doc in collection:
	    # Parse document with Beautiful Soup to remove unwanted tags.
            soup = BeautifulSoup(str(doc))

	    if soup.title:
		title = soup.title.findAll(text=True)
            if soup.th:
		th = soup.th.findAll(text=True)
            if soup.h1:
		h1 = soup.h1.findAll(text=True)
            if soup.h2:
		h2 = soup.h2.findAll(text=True)
	    if soup.h3:       
		h3 = soup.h3.findAll(text=True)
		s = ""
		for h in h3:
			s += " " + str(h.contents[0])
		print s
	    if soup.h4:
		h4 = soup.h4.findAll(text=True)
	    if soup.h5:
		h5 = soup.h5.findAll(text=True)
	    if soup.h6:
		h6 = soup.h6.findAll(text=True)
	    if soup.p:
		p = soup.p.findAll(text=True)
	    if soup.blockquote:
		blockquote = soup.blockquote.findAll(text=True)
	    if soup.td:
		td = soup.td.findAll(text=True)
#	    li = soup.li.findAll(text=True)
#	    label = soup.label.findAll(text=True)
#	    div = soup.div.findAll(text=True)
#	    section = soup.section.findAll(text=True)


#            writer.add_document(title=title, th=th, h1=h1, h2=h2, h3=s, h4=h4,
#                                h5=h5, h6=h6, p=p, blockquote=blockquote,
#                                td=td, li=li, label=label, div=div,
#                                section=section)

#            print "finishing add_document"

#        writer.commit()


