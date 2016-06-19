import os

OUT_DIRECTORY = 'word_clips'

def splitLine(line, videoid, personname):
    params = line.rstrip().split(',')
    start = params[0]
    length = params[1]
    # Find the out file name.
    outName = os.path.join(personname, 'word_clips', params[2])
    split = ('ffmpeg -i ' + os.path.join(personname, 'fullVideos',
        videoid + '.mp4') + ' -ss ' + start + ' -t ' + length + ' ' + outName)
    os.system(split)

def readFiles(personname):
    # Remove previous files
    os.system('rm -r ' + os.path.join(personname, 'word_clips'))
    os.makedirs(os.path.join(personname, 'word_clips'))

    manifestPath = os.path.join(personname, 'splitter_manifest')
    csvs = os.listdir(manifestPath)
    for fileName in csvs:
        with open(os.path.join(manifestPath, fileName), 'r') as f:
            for l in f:
                splitLine(l, fileName[:-4], personname)

readFiles('John_Oliver')
