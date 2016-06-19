from pymarkovchain import MarkovChain

import os
import sys

DATABASE_PATH = "markov_database"


def consolidateText(textDir):
    accumulatedText = ""
    for textFile in os.listdir(textDir):
        try:
            f = open(textDir + textFile, 'r')
            accumulatedText += f.read()
            f.close()
        except:
            sys.stdout.write("Error reading %s\n", textFile)
    return accumulatedText

def generateTEDTalk(minWords=100):
    textDir = "TED/fullTexts/"
    accumulatedText = consolidateText(textDir)
    markov = MarkovChain(DATABASE_PATH)
    markov.generateDatabase(accumulatedText, n=3)

    # Loop over sentence generation to make the talk
    talk = ""
    while len(talk.split()) < minWords:
        talk += markov.generateString()
        talk += ". "
    # Add applause at the end :)
    return talk.replace("(Applause)", "") + "(Applause)"

if __name__ == '__main__':
    if len(sys.argv) > 1:
        fname = sys.argv[1]
        fout = open(fname, 'w')
        fout.write(generateTEDTalk())
        fout.close()
    else:
        print(generateTEDTalk())

