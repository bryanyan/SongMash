from lxml import html,etree
from HTMLParser import HTMLParser

import csv
import os
import pytube
import requests

### Constants

# Documents directory where we can store the downloaded data
ROOT_DIR = "/Users/Scott/Documents/Hackathons/BattleOfTheHacks/SongMash"
CSV_DIR = "phraseCSVs"
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

def downloadVideoForId(videoId, videoFilename):
    """ Downloads and saves videos with the given ID """
    pass

def downloadTranscriptForId(videoId, csvFilename):
    """ Downloads the raw XML transcript for a video and converts it into a
        useable CSV file. """
    print("Downloading transcript for video " + str(videoId))

    # Retrieving the transcript will only work on videos with captions enabled
    transcriptUrl = "http://video.google.com/timedtext?lang=en&v=%s" % videoId
    try:
        rawData = requests.get(transcriptUrl)
        xmlTree = etree.fromstring(rawData.content)
    except:
        print("Failed to get transcript for: %s" % (videoId))
    csvString = HEADER_STRING + "\n"
    for child in xmlTree:
        cleanText = decodeHtml(child.text).replace(",","")
        rowString = "%s,%.3f,%.3f\n" %\
            (cleanText, float(child.get("start")), float(child.get("dur")))
        csvString += rowString
    try:
        f = open(csvFilename, "w")
        f.write(csvString)
        f.close()
    except:
        print("Failed to write CSV file for: %s" % (videoId))

def downloadAllData(videoIdList, speaker):
    """ Downloads both video and transcript for the given video ID """
    videoDir = "%s/%s/%s/" % (ROOT_DIR, speaker, VIDEO_DIR)
    csvDir = "%s/%s/%s/" % (ROOT_DIR, speaker, CSV_DIR)
    makeDirsIfNeeded(videoDir)
    makeDirsIfNeeded(csvDir)
    for videoId in videoIdList:
        videoFilename = "%s%s.mp4" % (videoDir, videoId)
        csvFilename = "%s%s.csv" % (csvDir, videoId)
        downloadVideoForId(videoId, videoFilename)
        downloadTranscriptForId(videoId, csvFilename)

def retrieveVideoIds(channelName, limit=2):
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


