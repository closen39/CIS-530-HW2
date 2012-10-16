# coding: utf-8
# Nate Close: closen@seas.upenn.edu
# Jason Mow: jmow@seas.upenn.edu

# Import the corpus reader
from nltk.tokenize import word_tokenize



# returns either the word itself in lowercase or 'num' if number
# TODO: make this less kludgy??
def word_transform(word):
    for char in word:
        if char.isdigit():
            return 'num'
    return word.lower()

def sent_transform(sent_string):
    tokens = word_tokenize(sent_string)
    ret = list()
    for token in tokens:
        ret.append(word_transform(token))
    return ret

# main method
def main():
    print "# 1.1\n>>> word_tranform('34,213.397')"
    print word_transform('34,213.397')
    print "\n\n# 1.1\n>>> word_tranform('General')"
    print word_transform('General')

    print "\n\n# 1.2\n>>> sent_tranform('Mr. Louis’s company (stock) raised to $15 per-share, growing 15.5% at 12:30pm.')"
    print sent_transform("Mr. Louis’s company (stock) raised to $15 per-share, growing 15.5% at 12:30pm.")

if  __name__ =='__main__':
    main()