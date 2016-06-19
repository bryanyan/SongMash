import csv, os
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
people = ['John_Oliver']

word_data = defaultdict(\
				lambda : defaultdict(\
					lambda : defaultdict(list)))

for person in people:
	word_timing_directory = os.path.join(person, 'word_timing')
	word_timing_files = [f for f in os.listdir(word_timing_directory) if os.path.isfile(os.path.join(word_timing_directory, f))]

	for word_timing_filename in word_timing_files:
		if '.csv' in word_timing_filename:
			videoid = word_timing_filename.split('.csv')[0]

			word_timing_filepath = os.path.join(personname, 'word_timing', word_timing_filename)
			with open(word_timing_filepath, 'rb') as word_timing_file:
				
				word_timing_reader = csv.reader(word_timing_file, delimeter=',')
				for row in word_timing_reader:
					word = row[2]
					time_start = row[3]
					length = row[4]
					is_first_word = row[5]

					if len(word_data[person][videoid][word]) == 0 or (not word_data[person][videoid][word][2] and is_first_word):
						# overwrite old record if
						# 1) there's no data
						# or 2) we found a first word (while the old record was not a first word)
						word_data[person][videoid][word] = row[3:6]


for personname in word_data:
	for videoid in word_data[personname]:
		data = []

		for word in word_data[personname][videoid]:
			row = word_data[personname][videoid][word][0:2] + [word + '_' + videoid + '.mp4'] # lop off is_first_word
			data.append(row)

		data.sort(key=lambda x: x[1])

		output_filepath = os.path.join(personname, 'splitter_manifest', videoid + '.csv')
		with open(output_filepath, 'wb') as csvfile:
			datawriter = csv.writer(csvfile, delimeter=',')
			datawriter.writerow(['start_time', 'length', 'rename_to'])
			datawriter.writerows(data)