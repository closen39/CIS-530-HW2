# Nate Close: closen@seas.upenn.edu
# Jason Mow: jmow@seas.upenn.edu

# Import the corpus reader
from nltk.corpus import PlaintextCorpusReader
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.probability import FreqDist
from math import log, sqrt

# gets all files in this directory and its sub-directories
def get_all_files(directory):
    files = PlaintextCorpusReader(directory, '.*')
    return files.fileids()

def get_sub_directories(directory):
    files = PlaintextCorpusReader(directory, ".*")
    dirs = list()
    for f in files.fileids():
        if "/" in f:
            if (f[:f.index("/")] not in dirs):
                dirs.append(f[:f.index("/")])
    return dirs

  # returns a list of all sentences in that file
def load_file_sentences(filepath):
    file1 = open(filepath)
    sent = file1.read()
    sent = sent.lower()
    return sent_tokenize(sent)  

# returns a list of all tokens in a file
def load_file_tokens(filepath):
    file1 = open(filepath)
    text = file1.read()
    return sent_transform(text)

# load all tokens in files within this directory
# should return list of tokens
def load_collection_tokens(directory):
    files = get_all_files(directory)
    li = list()
    for f in files:
        tokens = load_file_tokens(directory + "/" + f)
        li.extend(tokens)
    return li

def get_top_words_with_stoplist(path, n):
    # read in stoplist file
    stoplistfile = open('/home1/c/cis530/hw1/stoplist.txt')
    stoplist = [line.strip() for line in stoplistfile]

    files = get_all_files(path) # returns [] if path is a file
    fdist = FreqDist()
    if(len(files) == 0):
        for word in load_file_tokens(path):
            if(word not in stoplist):
                fdist.inc(word)
    else:
        for word in load_collection_tokens(path):
            if(word not in stoplist):
                fdist.inc(word)  
    li = fdist.keys()
    return li[:n]

def create_feature_space(inputlist):
    dict1 = {}
    index = 0
    for word in inputlist:
        if word not in dict1:
            dict1[word] = index
            index += 1
    return dict1

def vectorize(feature_space, string):
    tokens = sent_transform(string)
    li = list()
    for i in range(len(feature_space)):
        li.append(0)
    for word in tokens:
        if word in feature_space:
            li[feature_space[word]] = 1
    return li

def cosine_similarity(x, y):
    prodCross = 0.0
    xSquare = 0.0
    ySquare = 0.0
    for i in range(min(len(x), len(y))):
        prodCross += x[i] * y[i]
        xSquare += x[i] * x[i]
        ySquare += y[i] * y[i]
    if (xSquare == 0 or ySquare == 0):
        return 0.0
    return prodCross / (sqrt(xSquare) * sqrt(ySquare))

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
        self.vocab = list(set(self.words))

    # Probability determined by (count of ngram + 1) / (count of event + size of vocab)
    # Size of vocab is the number of unique tokens in the corpus
    def logprob(self, context, event):
        count = self.count_ngram(context, event)
        word_count = self.count_word(event)
        prob = (count + 1) / float((word_count + len(self.vocab)))
        return log(prob)

    # Counts occurences of a word in the corpus
    def count_word(self, event):
        events = [word for (context, word) in self.model if word is event]
        return len(events)

    # Couts occurences of a context and word in the corpus
    def count_ngram(self, context, event):
        ngrams = [(con, word) for (con, word) in self.model if (context, event) == (con, word)]
        return len(ngrams)

# trains a bigram language model
# seems approximately correct
# TODO: Debug why probability is slightly off for sample data
def build_bigram_from_files(file_names):
    docs = list()
    for file1 in file_names:
        f = open(file1)
        for line in f:
            docs.append(line.rstrip())

    # sentence tokenize all first lines
    samples = list()
    for doc in docs:
        samples.extend(sent_transform(doc))
    # make model
    model = NGramModel(samples, 2)
    return model

def get_fit_for_word(sent, word, model):
    words = sent_transform(sent)
    context = str()
    follower = str()
    for idx, wrd in enumerate(words):
        if wrd == '-blank-':
            context = words[idx-1]
        if words[idx-1] == '-blank-':
            follower = wrd
    lp1 = model.logprob((context,), word)
    lp2 = model.logprob((word,), follower)
    print lp1, lp2
    return lp1 + lp2

def get_all_bestfits(path):
    corpus = '/home1/c/cis530/hw2/data/corpus'
    data = [corpus + "/" + f for f in get_all_files(corpus)]
    model = build_bigram_from_files(data)
    files = get_all_files(path)
    ret = list()
    for f in files:
        probs = dict()
        f = open(path + "/" + f)
        sent = f.readline().rstrip()
        w1 = f.readline().rstrip()
        w2 = f.readline().rstrip()
        w3 = f.readline().rstrip()
        w4 = f.readline().rstrip()
        probs[w1] = get_fit_for_word(sent, w1, model)
        probs[w2] = get_fit_for_word(sent, w2, model)
        probs[w3] = get_fit_for_word(sent, w3, model)
        probs[w4] = get_fit_for_word(sent, w4, model)
        best = [k for k,v in probs.iteritems() if v is max(probs.values())]
        ret.extend(best)
    return ret

def get_cluto_matrix(file_names):
    # Get top words for each company
    corpus = '/home1/c/cis530/hw2/data/corpus'
    companies = get_sub_directories(corpus)
    top_words = dict()
    for co in companies:
        top_words[co] = get_top_words_with_stoplist(corpus + "/" + co, 200)

    # Flatten top words into single deduped list
    flattened = [item for sublist in top_words.values() for item in sublist]
    flattened = set(flattened)
    fs = create_feature_space(flattened)

    # Vectorize all documents
    doc_vectors = dict()
    for fname in file_names:
        f = open(fname)
        doc_vectors[fname] = vectorize(fs, f.read())

    matrix = []
    for id1, fname in enumerate(file_names):
        scores = list()
        for id2, fname2 in enumerate(file_names):
            scores.append(cosine_similarity(doc_vectors[fname], doc_vectors[fname2]))
        matrix.append(scores)

    print matrix
    # for k, v in top_words.iteritems():
    #     print "Company: " + str(k)
    #     print "\nWords: " + str(v[:5])

    # Get doc similarity for each file
    pass




def print_sentences_from_files(file_names, outfilename):
    # list of all sentences
    sents = list()
    # get sentence transform of all files
    for f in file_names:
        sents.extend(load_file_sentences(f))

    #list of formatted sents
    fsents = list()
    for sent in sents:
        string = ''
        for word in sent_transform(sent):
            string += word + ' '
        fsents.append(string + '\n')

    # open file for writing
    outfile = open(outfilename, "w")
    f.write(fsents)


# main method
def main():
    print "# 1.1.1\n>>> word_tranform('34,213.397')"
    print word_transform('34,213.397')
    print "\n\n# 1.1.1\n>>> word_tranform('General')"
    print word_transform('General')

    print "\n\n# 1.1.2\n>>> sent_tranform('Mr. Louis's company (stock) raised to $15 per-share, growing 15.5% at 12:30pm.')"
    print sent_transform("Mr. Louis's company (stock) raised to $15 per-share, growing 15.5% at 12:30pm.")

    samples = ['her', 'name', 'is', 'rio', 'and', 'she', 'dances', 'on', 'the', 'sand']
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

    print '\n\nlogprob(("her",), name) is ' + str(model.logprob(('her',), 'name'))

    file_names = ['file.txt', 'file2.txt']
    lm = build_bigram_from_files(file_names)
    print '\n\nbigram built - logprob of her name is ' + str(lm.logprob(('her',), 'name'))

    print '\n\nget_fit_for_word is ' + str(get_fit_for_word('her -blank- is rio and she dances on the sand', 'name', lm))

    print get_all_bestfits('/home1/c/cis530/hw2/data/wordfit/')

    get_cluto_matrix(file_names)

if  __name__ =='__main__':
    main()
