from ffmpy import FFmpeg
from concurrent.futures import ThreadPoolExecutor

import concurrent.futures
import os
import sys

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
            sys.stdout.write('Generating ' + outName + '\n')
            ff.run()

def processFile(manifestPath, personname, fileName):
    with open(os.path.join(manifestPath, fileName), 'r') as f:
        for l in f:
            splitLine(l, fileName[:-4], personname)

def readFiles(personname):
    if not os.path.exists(os.path.join(personname, 'word_clips')):
        os.makedirs(os.path.join(personname, 'word_clips'))

    manifestPath = os.path.join(personname, 'splitter_manifest')
    csvs = os.listdir(manifestPath)

    with ThreadPoolExecutor(max_workers=4) as executor:
        # Download the videos on separate threads
        ftrs = []
        for fileName in csvs:
            ftrs.append(executor.submit(processFile, manifestPath, personname, fileName))
        # Start the load operations and mark each future with its URL
        for future in concurrent.futures.as_completed(ftrs):
            try:
                # Wait for thread to finish
                future.result()
            except Exception as exc:
                sys.stdout.write('generated an exception: %s' % (exc))
        print("All threads completed!")





readFiles('TED')
