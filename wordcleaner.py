# Strips ugly charachters 

def isLetterClean(l):
    return l.isalpha() or l in ["'"]

def cleanWords(word_list):
    """ Removes non-alphabetic characters from words in list. """
    return [''.join(filter(isLetterClean, word)).lower().rstrip() for word in word_list]
