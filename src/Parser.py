'''
Created on 2013-10-15

@author: tina
'''

class Parser:
    def parse(self,path):
        input_file = open(path).read()
        #create a list which will contain the documents
        collection = dict()
        #Process the input file to extract document
        while 1:
            try:
                #extract document date as its key
                i = input_file.index("<DATE>") + 6
                j = input_file.index("</DATE>")
                filename = path + "." + input_file[i:j]
                #extract document content
                i = input_file.index("<BODY>") + 6
                j = input_file.index("</BODY>")
                #Append the document to our list
                collection[filename] = input_file[i:j]
                #Move forward on the input
                input_file = input_file[j+7:]
            except:
                print 'return from parsing'
            # if input_file.index("<BODY>") fails, we will end up here
            #  meaning the whole collection has been processed
                break
        return collection

        