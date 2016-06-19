# Script #2
# Assuming CSV in the following format:
# phrase, time start, duration
# Output in the following:
# Video ID, person name, word, time start, length (estimated), isFirstWord

from __future__ import division
from nltk.corpus import cmudict

import string
import sys
import os

# Uses Python NLP toolkit (NLTK) to approximate a word's syllable count
d = cmudict.dict()
def syllableCountWord(word):
    try:
        pronounciations = d[word.lower()]
        return len(list(y for y in pronounciations[0] if y[-1].isdigit()))
    except:
        return 0
    return 0

def readFile(path):
    with open(path, "rt") as f:
        return f.read()

def writeFile(path, contents):
    with open(path, "wt") as f:
        return f.write(contents)

def isLetterClean(l):
    return l.isalpha() or l in [",", "-"]

def cleanWords(word_list):
    """ Removes non-alphabetic characters from words in list. """
    return [''.join(filter(isLetterClean, word)) for word in word_list]

def parse(content, result):
    lines = content.split("\n")
    for line_num in range(len(lines)):
        if lines[line_num] == "": continue
        if line_num == 0: continue
        line_list = lines[line_num].split(",")
        # List format: [phrase, time start, duration]
        phrase = line_list[0]
        word_list = cleanWords(phrase.split(" "))
        # Use the number of syllables in words to approximate speech duration
        syllable_counts = [syllableCountWord(word) for word in word_list]
        total_syllables = sum(syllable_counts)
        if total_syllables == 0:
            return
        # Duration of entire phrase
        duration = round(float(line_list[2]), 2)
        time_start = round(float(line_list[1]), 2)
        # Approximate seconds per syllable of speech
        for word_num in range(len(word_list)):
            # new_line is the data for a single word
            new_line = [word_list[word_num]]
            nsyllables = syllable_counts[word_num]
            if nsyllables == 0:
                continue
            # Approximate time per syllable of speech * syllables in this word
            word_time = duration * nsyllables / float(total_syllables)
            new_line.append(str(round(time_start, 2)))
            new_line.append(str(round(word_time, 2)))
            # Flag for first word (considered more accurate)
            new_line.append(str(word_num == 0))
            assert(len(new_line) == 4)
            result.append(new_line)
            time_start += word_time
    return


def write(origin, destination):

    file_content = readFile(origin)
    result_list = [ ]
    parse(file_content, result_list)
    result = ""
    for line in result_list:
        result = result + ",".join(line) + "\n"
    writeFile(destination, result) # TODO temporary

    return


# assumes there is a top-level directory named "data" containing everything
def main():
    checked = set()
    current_path = os.path.dirname(os.path.abspath(__file__))
    current_path = os.path.join(current_path, "TED")
    # for speaker in os.listdir(current_path):
        # fetch files from here
        # origin = current_path+os.sep+speaker+os.sep+"phraseCSVs"
        # destination = current_path+os.sep+speaker+os.sep+"word_timing"
    origin = os.path.join(current_path, "phraseCSVs")
    if not ("word_timing" in os.listdir(current_path)):
        os.mkdir(os.path.join(current_path, "word_timing"))
    destination = os.path.join(current_path, "word_timing")
    for data in os.listdir(origin):
        filepath = os.path.join(origin, data)
        if not (filepath in checked): 
            write(filepath, os.path.join(destination, data))
            checked.add(filepath)
    return

main()
