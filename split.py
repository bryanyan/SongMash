import os
from ffmpy import FFmpeg

OUT_DIRECTORY = 'word_clips'

def splitLine(line, videoid, personname):
    params = line.rstrip().split(',')
    if len(params) == 3:
        start = params[0]
        length = params[1]
        # Find the out file name.
        outName = os.path.join(personname, 'word_clips', params[2])
        if not os.path.isfile(outName):
            ff = FFmpeg(
                inputs={os.path.join(personname, 'fullVideos',
                    videoid + '.mp4'): None},
                outputs={outName: '-ss ' + start + ' -t ' + length}
            )
            print('Generating ' + outName)
            ff.run()

def readFiles(personname):
    if not os.path.exists(os.path.join(personname, 'word_clips')):
        os.makedirs(os.path.join(personname, 'word_clips'))

    manifestPath = os.path.join(personname, 'splitter_manifest')
    csvs = os.listdir(manifestPath)
    for fileName in csvs:
        with open(os.path.join(manifestPath, fileName), 'r') as f:
            for l in f:
                splitLine(l, fileName[:-4], personname)

readFiles('TED')
