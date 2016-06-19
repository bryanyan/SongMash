# Script #2
# Assuming CSV in the following format: 
# Video id, person name, phrase, time start, duration
# Output in the following: 
# Video ID, person name, word, time start, length (estimated), isFirstWord 
from __future__ import division
import string
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
        if lines[line_num] == "": continue
        line_list = lines[line_num].split(", ")
        # List format: [video id, person name, phrase, time start, duration]
        print line_list
        phrase = line_list[2]
        word_list = phrase.split(" ")
        for word_num in range(len(word_list)):
            new_line = [line_list[0], line_list[1], word_list[word_num]]
            duration = round(float(line_list[4]), 2)
            time_start = round(float(line_list[3]), 2)
            length = duration/float(len(word_list)) #is a double
            new_line.append(str(round(time_start + word_num*(length), 2)))
            new_line.append(str(round(length, 2)))
            new_line.append(str(word_num == 0))
            assert(len(new_line) == 6)
            result.append(new_line)
    
    return        


def main():
    if len(sys.argv) != 2:
        sys.exit("Must pass in exactly 1 file path")
    path = sys.argv[1]
    file_content = readFile(path)
    result_list = [ ]
    parse(file_content, result_list)
    result = ""
    for line in result_list:
        result = result + ", ".join(line) + "\n"
    # yes i make assumptions such as the file name will end in .txt
    # yes i'm the definition of bad practice
    writeFile(path[:len(path)-4]+"_test.txt", result) # TODO temporary

main()
    
