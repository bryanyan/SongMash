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
		stripped = line.rstrip().replace('.', ' _').replace(',', ' _')
		words = stripped.split(' ')
		for w in words:
			files.append(w.rstrip() + FILE_TYPE)
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
	os.system('ffmpeg -i ' + VIDEO_DIRECTORY + i +
		' -c copy -f mpegts ' +
		VIDEO_DIRECTORY + i + '.ts')
# Remove the previous output file first.
if os.path.isfile('output.mp4'):
	os.system('rm output.mp4')
# Generate the command for concatting the mpegs.
merge = 'ffmpeg -i "concat:'
for i in foundFiles:
	merge += VIDEO_DIRECTORY + i + '.ts|'
merge = merge[:-1]
merge += '" -c copy -bsf:a aac_adtstoasc output.mp4'
os.system(merge)
# Clean up the intermediate mpegs.
for i in unique:
	os.system('rm ' + VIDEO_DIRECTORY + i + '.ts')
# Log failed files.
for i in notFound:
	print('Couldn\'t find ' + i)
