import string


class Analyzer(object):
    '''
    for each input string, process it and extract tokens
    '''
    def __init__(self):
        pass

    def getstopwords(self):
        stopw_file = open('stopw.txt')
        stopw_file_string = stopw_file.read()
        stop_words = stopw_file_string.split(",")
        stop_list = [x.strip() for x in stop_words]
        return stop_list

    def tokenize(self, doc):
        #stop_list = self.getstopwords()
        tokens = list()
        #remove capital letters, punctuation, newline and tab
        doc = doc.lower().translate(None, string.punctuation.join('\n\t'))
        #remove numbers
        doc = ''.join([i for i in doc if not i.isdigit()])
        #split tokens on spaces
        for token in doc.split(" "):
            #if not token in stop_list:
            tokens.append(token)
        return tokens