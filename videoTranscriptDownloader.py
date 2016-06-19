from lxml import html,etree
from HTMLParser import HTMLParser
from pytube import YouTube
from concurrent.futures import ThreadPoolExecutor

import concurrent.futures
import csv
import os
import pytube
import requests
import sys # sys print function on threads

### Constants

# Documents directory where we can store the downloaded data
ROOT_DIR = os.path.dirname(os.path.realpath(__file__)) + "/"
CSV_DIR = "phraseCSVs"
TXT_DIR = "fullTexts"
VIDEO_DIR = "fullVideos"
HEADER_STRING = "phrase,start,duration"

### Utilities

htmlDecoder = HTMLParser()
def decodeHtml(rawHtml):
    """ Removes escape characters from HTML """
    return htmlDecoder.unescape(rawHtml)

def makeDirsIfNeeded(dirName):
    if not os.path.exists(dirName):
        os.makedirs(dirName)

def downloadVideoForId(videoId, videoDir):
    """ Downloads and saves videos with the given ID """
    if os.path.exists(videoDir + videoId + ".mp4"):
        sys.stdout.write("Using cached video for " + videoId + "\n")
        return
    sys.stdout.write("Downloading video " + videoId + "\n")
    videoUrl = "http://youtube.com/watch?v=%s" % videoId
    videoRsc = YouTube(videoUrl)
    videoRsc.set_filename("%s" % videoId)
     # Downloads low resolution mp4 for testing
    videoRsc.get("mp4", "360p").download(videoDir)

def downloadTranscriptForId(videoId, csvFilename, textFilename):
    """ Downloads the raw XML transcript for a video and converts it into a
        useable CSV file. """
    sys.stdout.write("Downloading transcript for video " + videoId + "\n")
    # Retrieving the transcript will only work on videos with captions enabled
    transcriptUrl = "http://video.google.com/timedtext?lang=en&v=%s" % videoId
    try:
        rawData = requests.get(transcriptUrl)
        xmlTree = etree.fromstring(rawData.content)
    except:
        sys.stdout.write(">> Failed to get transcript for: %s\n" % (videoId))
    csvString = HEADER_STRING + "\n"
    textString = ""
    for child in xmlTree:
        # Remove HTML escapes
        cleanText = decodeHtml(child.text).replace(",","")
        # Replace newlines with spaces for CSV consistency
        cleanText = cleanText.replace("\n"," ")
        rowString = "%s,%.3f,%.3f\n" %\
            (cleanText, float(child.get("start")), float(child.get("dur")))
        csvString += rowString
        # Copy regular text for the text file
        textString += cleanText + " "
    try:
        f = open(csvFilename, "w")
        f.write(csvString)
        f.close()
    except:
        sys.stdout.write(">> Failed to write CSV file for: %s\n" % (videoId))
    try:
        f = open(textFilename, "w")
        f.write(textString)
        f.close()
    except:
        sys.stdout.write(">> Failed to write text file for: %s\n" % (videoId))


def downloadAllData(videoIdList, speaker):
    """ Downloads both video and transcript for the given video ID """
    csvDir = "%s/%s/%s/" % (ROOT_DIR, speaker, CSV_DIR)
    textDir = "%s/%s/%s/" % (ROOT_DIR, speaker, TXT_DIR)
    videoDir = "%s/%s/%s/" % (ROOT_DIR, speaker, VIDEO_DIR)
    makeDirsIfNeeded(csvDir)
    makeDirsIfNeeded(textDir)
    makeDirsIfNeeded(videoDir)

    # Concurrent downloads based on
    # https://docs.python.org/3/library/concurrent.futures.html
    with ThreadPoolExecutor(max_workers=6) as executor:
        # Download the videos on separate threads
        ftrs = []
        for videoId in videoIdList:
            csvFilename = "%s%s.csv" % (csvDir, videoId)
            textFilename = "%s%s.txt" % (textDir, videoId)
            ftrs.append(executor.submit(downloadVideoForId, videoId, videoDir))
            ftrs.append(executor.submit(
                downloadTranscriptForId, videoId, csvFilename, textFilename))
        # Start the load operations and mark each future with its URL
        for future in concurrent.futures.as_completed(ftrs):
            try:
                # Wait for thread to finish
                future.result()
            except Exception as exc:
                print('generated an exception: %s' % (exc))
        print("All threads completed!")

def retrieveVideoIds(channelName, limit=10):
    """ Retrieves up to `limit` videos and transcripts from the channel """
    channelUrl = "https://www.youtube.com/user/%s/videos" % channelName
    linkStart = "/watch?v="
    rawPage = requests.get(channelUrl)
    htmlTree = html.fromstring(rawPage.content)
    videoIds = []
    i = 0
    for link in htmlTree.cssselect('.yt-uix-tile-link'):
        i += 1
        if i > limit:
            break
        rawHref = link.get('href')
        if linkStart in rawHref:
            videoIds.append(rawHref.replace(linkStart, ""))
    return videoIds

def lastWeekTonight():
    lwtIds = retrieveVideoIds("LastWeekTonight")
    downloadAllData(lwtIds, "John Oliver")

def tedTalks():
    tedIds = retrieveVideoIds("TEDtalksDirector")
    downloadAllData(tedIds, "TED")

if __name__ == '__main__':
    tedTalks()


