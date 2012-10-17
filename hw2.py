# coding: utf-8
# Nate Close: closen@seas.upenn.edu
# Jason Mow: jmow@seas.upenn.edu

# Import the corpus reader
from nltk.tokenize import word_tokenize


# returns either the word itself in lowercase or 'num' if number
# Returns numerical delimiter punctuation as a word if appears alone (ie. punctuation)
# Checks all chars of the word to be number, comma, or period
#   If any other char appears, return word in lower case
#   Else return num
def word_transform(word):
    if word == ',' or word == '.':
        return word
    for char in word:
        if not char.isdigit() and not char == ',' and not char == '.':
            return word.lower()
    return 'num'

def sent_transform(sent_string):
    tokens = word_tokenize(sent_string)
    ret = list()
    for token in tokens:
        ret.append(word_transform(token))
    return ret

# creates ngram tuples of (context, word)
def make_ngram_tuples(samples, n):
    ret = list()
    for idx, word in enumerate(samples):
        if idx < n-1:
            continue
        if n != 1:
            context = tuple(samples[idx-n+1:idx])
        else:
            context = None
        ret.append(tuple([context, word]))
    return ret

class NGramModel:
    def __init__(self, training_data, n):
        self.words = training_data
        self.model = make_ngram_tuples(training_data, n)
        
    def logprob(self, context, event):
        pass

    def count_word(self, event):
        events = [word for (context, word) in self.model if word is event]
        return len(events)

    def count_ngram(self, context, event):
        ngrams = [(con, word) for (con, word) in self.model if (context, event) == (con, word)]
        return len(ngrams)

# main method
def main():
    print "# 1.1\n>>> word_tranform('34,213.397')"
    print word_transform('34,213.397')
    print "\n\n# 1.1\n>>> word_tranform('General')"
    print word_transform('General')

    print "\n\n# 1.2\n>>> sent_tranform('Mr. Louis's company (stock) raised to $15 per-share, growing 15.5% at 12:30pm.')"
    print sent_transform("Mr. Louis's company (stock) raised to $15 per-share, growing 15.5% at 12:30pm.")

    samples = ['her', 'name', 'is', 'rio', 'and', 'she', 'dances', 'on', 'the', 'her', 'name', 'is', 'jane', 'sand']
    print "\n\n#1.3\n>>>make_ngram_tuples"
    print "Samples = "
    print samples
    print "\n"
    print make_ngram_tuples(samples, 1)
    print "\n"
    print make_ngram_tuples(samples, 2)
    print "\n"
    print make_ngram_tuples(samples, 3)
    print "\n\n"

    model = NGramModel(samples, 2)
    print model.model
    print '\ncount of her is ' + str(model.count_word('name'))

    print '\n\ncount of "her name" is ' + str(model.count_ngram(('her',), 'name'))
    print '\n\ncount of "is rio" is ' + str(model.count_ngram(('is',), 'rio'))


if  __name__ =='__main__':
    main()