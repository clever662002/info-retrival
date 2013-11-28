#import sys
#import glob
#import errno
from bs4 import BeautifulSoup, Comment, Doctype
import os


class Parser:
	def parse(self, path):
        #create a list which will contain the documents
#        collection = list()
        #Process the input file to extract documents
		for filename in os.listdir(path):
			input_file = open(path + filename)
			soup = BeautifulSoup(input_file)
			blacklist = ['script','meta', 'link', 'style', 'a','meta','button','img','iframe','br']
			# Delete DOCTYPE declaration
   			#items = [item for item in soup.contents if isinstance(item, Doctype)]
    			#del items
    		for tag in soup.findAll(True):
			if tag.name.lower() in blacklist:
				tag.extract()
			for attribute in ["accesskey", "border", "bordercolor", "cellpadding", "cellspacing",
				"width", "height", "colspan", "valign", "type", "align", "action", "style"]:
				del tag[attribute]
			if soup:
				continue
			# scripts can be executed from comments in some cases
			comments = soup.findAll(text=lambda text:isinstance(text, Comment))
			for comment in comments:
				comment.extract()
            	print soup.prettify()
		print '********************************************'
#		return collection

# main function
if __name__ == '__main__':
    collection = list()
    parser = Parser()
    path = "/home/tina/projects/test/"
    parser.parse(path)
'''
class Parser:
    def parse(self, path):
        input_file = open(path).read()
        #create a list which will contain the documents
        collection = list()
        #Process the input file to extract document
        while 1:
            try:
                #extract document content
                i = input_file.index("<BODY>") + 6
                j = input_file.index("</BODY>")
                #Append the document to our list
                collection.append(input_file[i:j])
                #Move forward on the input
                input_file = input_file[j + 7:]
            except:
            # if input_file.index("<BODY>") fails, we will end up here
            # meaning the whole collection has been processed
                break
        return collection
'''
