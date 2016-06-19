# Script #2
# Assuming CSV in the following format: 
# Video id, person name, phrase, time start, duration
# Output in the following: 
# Video ID, person name, word, time start, length (estimated), isFirstWord 

from __future__ import division
import string
import sys
import os






def readFile(path):
    with open(path, "rt") as f:
        return f.read()

def writeFile(path, contents):
    with open(path, "wt") as f:
        return f.write(contents)

def parse(content, result):
    lines = content.split("\n")
    for line_num in range(len(lines)):
        if lines[line_num] == "": continue
        line_list = lines[line_num].split(",")
        # List format: [phrase, time start, duration]
        print line_list
        phrase = line_list[0]
        word_list = phrase.split(" ")
        for word_num in range(len(word_list)):
            new_line = [word_list[word_num]]
            duration = round(float(line_list[2]), 2)
            time_start = round(float(line_list[1]), 2)
            length = duration/float(len(word_list)) #is a double
            new_line.append(str(round(time_start + word_num*(length), 2)))
            new_line.append(str(round(length, 2)))
            new_line.append(str(word_num == 0))
            assert(len(new_line) == 4)
            result.append(new_line)
    
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
    for speaker in os.listdir("data/"):
        # fetch files from here
        origin = "data"+os.sep+speaker+os.sep+"phraseCSVs"
        destination = "data"+os.sep+speaker+os.sep+"word_timing"
        for data in os.listdir(origin):
            filepath = os.path.join(origin, data)
            if not (filepath in checked): 
                write(filepath, os.path.join(destination, data))
                checked.add(filepath)
    return

main()
