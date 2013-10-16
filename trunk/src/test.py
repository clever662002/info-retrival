'''
Created on 2013-10-16

@author: tina
'''
import string
mystr = 'abds,bbs \n ccd.'.translate(None,string.punctuation.join('\n\t'));
print mystr