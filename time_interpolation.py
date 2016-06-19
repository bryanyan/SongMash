# Script #2
# Assuming CSV in the following format: 
# Video id, person name, phrase, time start, duration
# Output in the following: 
# Video ID, person name, word, time start, length (estimated), isFirstWord 
import string
from __future__ import division
import sys

def readFile(path):
    with open(path, "rt") as f:
        return f.read()

def writeFile(path, contents):
    with open(path, "wt") as f:
        return f.write(contents)


def parseCSV(path): 
    pass

def parse(content, result):
    lines = content.split("\n")
    for line_num in range(len(lines)):
        line_list = lines[line_num].split(", ")
        # List format: [video id, person name, phrase, time start, duration]
        phrase = line_list[2]
        word_list = phrase.split(" ")
        for word_num in range(len(word_list)):
            new_line = [line_list[0], line_list[1], word_list[word_num]]
            duration = round(float(line_list[4]), 2)
            time_start = rount(float(line_list[3]), 2)
            length = duration/float(len(word_list)) #is a double
            new_line.append(round(time_start + word_num*(length), 2))
            new_line.append(round(length, 2))
            if (word_num == 0): 
                new_line.append(True)
            assert(len(new_line) == 6)
            result.append(new_line)
    
    return        


def main():
    if len(sys.argv) != 1:
        sys.exit("Must pass in exactly 1 file path")
    path = sys.argv[0]
    file_content = readFile(path)
    result = [ ]
    parse(file_content, result)
    writeFile(path, result)
    
