import os
from whoosh import index
from whoosh.fields import *
from bs4 import BeautifulSoup

class Indexing:

    def __init__(self):
        self.schema = Schema(path=ID(stored=True),
                        title=TEXT(stored=True, field_boost=5.0),
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
        for key, value in collection.iteritems():
            #get document's path which is a key in dict
            path = u"".join(key)
            # print path
            # Parse document with Beautiful Soup to remove unwanted tags.
            soup = BeautifulSoup(str(value))

            if soup.title:
                title = u" ".join(soup.title.findAll(text=True))
            else:
                title = None
            if soup.th:
                th = u" ".join(soup.th.findAll(text=True))
            else:
                th = None
            if soup.h1:
                h1 = u" ".join(soup.h1.findAll(text=True))
            else:
                h1 = None
            if soup.h2:
                h2 = u" ".join(soup.h2.findAll(text=True))
            else:
                h2 = None
            if soup.h3:
                h3 = u" ".join(soup.h3.findAll(text=True))
            else:
                h3 = None
            if soup.h4:
                h4 = u" ".join(soup.h4.findAll(text=True))
            else:
                h4 = None
            if soup.h5:
                h5 = u" ".join(soup.h5.findAll(text=True))
            else:
                h5 = None
            if soup.h6:
                h6 = u" ".join(soup.h6.findAll(text=True))
            else:
                h6 = None
            if soup.p:
		p = ""
		for node in soup.findAll('p'):
    			p += u" ".join(node.findAll(text=True))
            else:
                p = None
            if soup.blockquote:
                blockquote = u" ".join(soup.blockquote.findAll(text=True))
            else:
                blockquote = None
            if soup.td:
                td = u" ".join(soup.td.findAll(text=True))
            else:
                td = None
            if soup.li:
                li = u" ".join(soup.li.findAll(text=True))
            else:
                li = None
            if soup.label:
                label = u" ".join(soup.label.findAll(text=True))
            else:
                label = None
            if soup.div:
                div = u" ".join(soup.div.findAll(text=True))
            else:
                div = None
            if soup.section:
                section = u" ".join(soup.section.findAll(text=True))
            else:
                section = None

            writer.add_document(path=path, title=title, th=th, h1=h1,
                                h2=h2, h3=h3, h4=h4, h5=h5, h6=h6,
                                p=p, blockquote=blockquote,
                                td=td, li=li, label=label, div=div,
                                section=section)

            print "finishing add_document"

        writer.commit()

