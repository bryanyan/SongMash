from lxml import html
import requests

ROOT_DIR = "~/tmp"


def downloadVideoForId(videoId, videoFilename):
    pass

def downloadTranscriptForId(videoId, csvFilename):
    print("Downloading transcript for video " + str(videoId))

def downloadAllData(videoIdList, personName):
    for videoId in videoIdList:
        videoFilename = "%s/%s/videos/%s.mp4" % (ROOT_DIR, personName, videoId)
        transcriptFilename = \
            "%s/%s/transcripts/%s.mp4" % (ROOT_DIR, personName, videoId)
        downloadVideoForId(videoId, videoFilename)
        downloadTranscriptForId(videoId, transcriptFilename)

def retrieveVideoIds(channelName):
    channelUrl = "https://www.youtube.com/user/%s/videos" % channelName
    linkStart = "/watch?v="
    rawPage = requests.get(channelUrl)
    htmlTree = html.fromstring(rawPage.content)
    videoIds = []
    for link in htmlTree.cssselect('.yt-uix-tile-link'):
        rawHref = link.get('href')
        if linkStart in rawHref:
            videoIds.append(rawHref.replace(linkStart, ""))
    return videoIds

def lastWeekTonight():
    lwtIds = retrieveVideoIds("LastWeekTonight")
    downloadAllData(lwtIds, "John Oliver")

if __name__ == '__main__':
    lastWeekTonight()


