# VidSmash

This project was made by the [ScottyLabs](https://scottylabs.org/) TartanHacks team, consisting of Scott Krulcik,
Emily Newman, Bryan Yan, Ian Lo, and Ajay Jain (MIT '20) at a16z's Battle of the Hacks v3 in June 2016.

VidSmash parses a collection of YouTube videos into re-usable clips that can be smashed together into making entirely new videos. It was inspired by videos of policitians singing pop songs, which must be meticulously stitched together. VidSmash makes it easy to stitch similar videos for songs, but also other projects, such as markov-chain generated TED talks.

# How It Works

## Clip Generation

First, we pick a source for a list of YouTube videos. For our demo, we scraped the TED channel. Next, we try to download transcripts for those videos (which are not always accessible). YouTube transcripts give the start times of phrases, but not individual words. So in order to stick words together, we use Natural Language Processing (NLP) to approximate the number of syllables in each word and estimate the speaking times of individual words.

These words are then intelligently split into re-useable clips, which try to use the most accurately timed words (the first words of closed-caption phrases) wherever possible.

Additionally, we add the text of the word to the bottom of the video to aid in its interpretation.

## Clip Merging

Arbitrary text, song data, or markov-generated TED talks can be entered into our web application, and split into words that need to be loaded. Using ffmpeg, we were able to merge our small snippets together.

## TED Talk Generation

Markov Chains are a tool from probablity theory that allow us to predict state transitions. If we consider a sequence of words as a beginning state, and the next word as the transition, we can use a large database of TED talk text to generate a TED-esque piece of text. This text can then be fed into our video generator to create an original TED video.

### Dependencies (incomplete)
* [Moviepy](https://pypi.python.org/pypi/moviepy)
* FFMPEG
* [Pytube](https://pypi.python.org/pypi/pytube)
* [lxml](http://lxml.de)
* [Requests](http://docs.python-requests.org/en/master)
* [PyMarkovChain](https://pypi.python.org/pypi/PyMarkovChain)
* [ffmpy](https://pypi.python.org/pypi/ffmpeg)
* [Natural Language Toolkit](http://www.nltk.org)
* ...and more (possibly)




