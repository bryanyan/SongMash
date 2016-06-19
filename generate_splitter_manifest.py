import csv, os
import string
from collections import defaultdict

"""
personname: {
	videoid: {
		word: [time_start, length, isFirstWord],
		word: [time_start, length, isFirstWord],
		...
	}
}
"""

# Change these as needed
people = ['TED']

word_data = defaultdict(\
				lambda : defaultdict(\
					lambda : defaultdict(list)))

for person in people:
	word_timing_directory = os.path.join(person, 'word_timing')
	word_timing_files = [f for f in os.listdir(word_timing_directory) if os.path.isfile(os.path.join(word_timing_directory, f))]

	for word_timing_filename in word_timing_files:
		if '.csv' in word_timing_filename:
			videoid = word_timing_filename.split('.csv')[0]

			word_timing_filepath = os.path.join(person, 'word_timing', word_timing_filename)
			with open(word_timing_filepath, 'rb') as word_timing_file:

				word_timing_reader = csv.reader(word_timing_file, delimiter=',')
				for row in word_timing_reader:
					word = row[0].translate(None, string.punctuation).lower()
					translated = [row[1], row[2]]
					is_first_word = row[3] == 'True'

					# if len(word_data[person][videoid][word]) == 0 or is_first_word:
					if is_first_word:
						# overwrite old record if
						# 1) there's no data
						# or 2) we found a first word (while the old record was not a first word)
						word_data[person][videoid][word] = translated


for personname in word_data:
	for videoid in word_data[personname]:
		data = []

		for word in word_data[personname][videoid]:
			row = word_data[personname][videoid][word][0:2] + [word + '.mp4'] # lop off is_first_word
			data.append(row)

		data.sort(key=lambda x: x[1])

		output_filepath = os.path.join(personname, 'splitter_manifest', videoid + '.csv')
		if not os.path.exists(os.path.join(personname, 'splitter_manifest')):
		    os.makedirs(os.path.join(personname, 'splitter_manifest'))
		with open(output_filepath, 'wb') as csvfile:
			datawriter = csv.writer(csvfile, delimiter=',')
			datawriter.writerows(data)
