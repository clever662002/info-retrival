import os
from whoosh import index
from whoosh.fields import *
from bs4 import BeautifulSoup

class Indexing:

    def __init__(self):
        self.schema = Schema(path=ID(stored=True),
                        title=TEXT(vector=True, stored=True, field_boost=5.0),
                        th=TEXT(vector=True, stored=True, field_boost=4.0),
                        h1=TEXT(vector=True, stored=True, field_boost=4.0),
                        h2=TEXT(vector=True, stored=True, field_boost=3.0),
                        p=TEXT(vector=True, stored=True, field_boost=3.0),
                        blockquote=TEXT(vector=True, stored=True, field_boost=3.0),
                        td=TEXT(vector=True, stored=True, field_boost=3.0),
                        li=TEXT(vector=True, stored=True, field_boost=3.0),
                        h3=TEXT(vector=True, stored=True, field_boost=2.0),
                        label=TEXT(vector=True, stored=True, field_boost=2.0),
                        span=TEXT(vector=True, stored=True, field_boost=2.0),
                        h4=TEXT(vector=True, stored=True, field_boost=2.0),
                        h5=TEXT(vector=True, stored=True, field_boost=2.0),
                        h6=TEXT(vector=True, stored=True, field_boost=2.0),
                        div=TEXT(vector=True, stored=True),
                        section=TEXT(vector=True, stored=True),
			content=TEXT(vector=True))

    def process(self, collection):
        w_list = ["title", "th", "h1", "h2", "p",
             "blockquote", "td", "li", "h3", "label",
             "span", "h4", "h5", "h6", "div", "section"]

        tc = dict()

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
            soup = BeautifulSoup(str(value)) # value = HTML content of document

            for e in w_list:
                if soup.findAll(e):
                    res = " "
                    for node in soup.findAll(e):
                        res += u" ".join(node.findAll(text=True))
                    tc[e] = res
                else:
                    tc[e] = None

            writer.add_document(path=path, title=tc["title"], th=tc["th"],
                                h1=tc["h1"], h2=tc["h2"], h3=tc["h3"],
                                h4=tc["h4"], h5=tc["h5"], h6=tc["h6"],
                                p=tc["p"], blockquote=tc["blockquote"],
                                td=tc["td"], li=tc["li"], label=tc["label"], span=tc["span"],
                                div=tc["div"], section=tc["section"], content=unicode(soup))

        writer.commit()

