from ffmpy import FFmpeg
from wordcleaner import cleanWords

import os
import glob
import sys

VIDEO_DIRECTORY = './TED/word_clips/'
FILE_TYPE = '.mp4'

if len(sys.argv) < 2:
	print('No text file specified.')
	sys.exit()
textFile = sys.argv[1]

files = []
notFound = []

# Read the input file.
with open(textFile, 'r') as f:
	# Generate the list of files.
	for line in f:
		# Remove punctuation and whitespace. Add a wait in periods and commas.
                line = line.replace('.', ' XPAUSE').replace(',', ' XPAUSE')
                words = line.rstrip().split(' ')
                words = cleanWords(words)
		for w in words:
                    if len(w) > 0:
			  files.append(w + FILE_TYPE)

# Append the ending since some audio gets cut off.
files.append('_' + FILE_TYPE)

foundFiles = []
for i in files:
	if os.path.isfile(VIDEO_DIRECTORY + i):
		foundFiles.append(i)
	else:
		notFound.append(i)

# Keep a set of unique filenames so we don't convert files more than once.
unique = list(set(foundFiles))

# Convert to an mpeg format that can be concatted.
for i in unique:
	ff = FFmpeg(
		inputs={VIDEO_DIRECTORY + i: None},
		outputs={VIDEO_DIRECTORY + i + '.ts': '-c copy -f mpegts'}
	)
	ff.run()
# Remove the previous output file first.
if os.path.isfile('output.mp4'):
	os.system('rm output.mp4')
# Generate the command for concatting the mpegs.
inputs = 'concat:'
for i in foundFiles:
	inputs += VIDEO_DIRECTORY + i + '.ts|'
inputs = inputs[:-1] + ''
ff = FFmpeg(
	inputs={inputs: None},
	outputs={'output.mp4': '-c copy -bsf:a aac_adtstoasc'}
)
ff.run()
# Clean up the intermediate mpegs.
for i in unique:
	os.system('rm ' + VIDEO_DIRECTORY + i + '.ts')
# Log failed files.
for i in notFound:
	print('Couldn\'t find ' + i)
