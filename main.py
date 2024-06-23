from ast import Return
from pytube import YouTube
import threading, datetime, os
from logger import Logger
from audioExtractor import AudioExtractor
from audioTranscriber import AudioTranscriber
from sentimentAnalyser import SentimentAnalysis
from translator import SpanishTranslator
from emotionExtractor import EmotionExtractor

#to check the downloaded videos
from os import listdir
from os.path import isfile, join

limiter = threading.BoundedSemaphore(5)
data_lock = threading.Lock() # mutex

def download_video(url, index):
    limiter.acquire()
    yt = YouTube(url)
    stream = yt.streams.get_highest_resolution()
    print(f"Thread {index}: Downloading video: {yt.title}")
    stream.download(output_path="video_output")
    print(f"Thread {index} : Download completed: {yt.title}")
    current_timestamp = datetime.datetime.now()
    current_timestamp = current_timestamp.strftime('%H:%M, %d %B %Y')
    thread_log = Logger(yt.title,index,current_timestamp,url,True)
    print(thread_log.getData())
    data_lock.acquire()
    thread_log.recordData()
    data_lock.release()
    limiter.release()
    Return


## READ URLs from video_urls.txt and put them on a list

url_list = []
with open("video_urls.txt", "r") as f:
    for line in f:
        url_list.append(line)

# Clear the Log file if it exists
        if os.path.exists('download_log.txt'):
            with open('download_log.txt', 'w') as file:
                file.write("")

## Serially Download videos from the list

#for i in url_list:
#    download_video(i)

## Parallel Download videos from the list
downloadThreads = []
for i in range(len(url_list)):
    thread = threading.Thread(target=download_video, args=(url_list[i],i,))
    downloadThreads.append(thread)
    thread.start()

# Wait for all threads to complete
for thread in downloadThreads:
    thread.join()

#check the videofiles
videofiles = [f for f in listdir('video_output') if isfile(join('video_output', f))]
audioExtracted = []
audioExtractThreads = []
'''
#Serially extract audio from the downloaded videos
for video in videofiles:
    thread_audioExtractor = AudioExtractor()
    video_path = join("video_output", video)  # Ensure full path is passed
    try:
        audioExtracted.append(thread_audioExtractor.extractAudio(video_path))
    except Exception as e:
        print(f"Error extracting audio from {video_path}: {e}")
'''
#Parallel extract audio from the downloaded videos
for i in range(len(videofiles)):
    video_path = join("video_output", videofiles[i])  # Ensure full path is passed
    thread = threading.Thread(target=AudioExtractor().extractAudio, args=(video_path,audioExtracted,))
    audioExtractThreads.append(thread)
    thread.start()

# Wait for all threads to complete
for thread in audioExtractThreads:
    thread.join()

print(audioExtracted)

#Save location of transcribed audios

transcribedAudio = []

#Serially transcribe the audio files
'''for audio in audioExtracted:
    thread_audioTranscribed = AudioTranscriber()
    #text_path = join("extracted_audio",audio)
    try:
        transcribedAudio.append(thread_audioTranscribed.transcribe(audio))
    except Exception as e:
        print(f"Error transcribing audio from {audio}: {e}")
'''
#Parallel transcribe the audio files
transcribeThreads = []
for i in range(len(audioExtracted)):
    thread = threading.Thread(target=AudioTranscriber().transcribe, args=(audioExtracted[i],transcribedAudio,))
    transcribeThreads.append(thread)
    thread.start()


# Wait for all threads to complete
for thread in transcribeThreads:
    thread.join()

print(f"THE TRANSCRIBED AUDIO PATHTS ARE: {transcribedAudio}")
#Save location of sentiment analysis

sentimentAnalysis = []

#Serially sentiment analysis the text files
for text in transcribedAudio:
    thread_sentimentAnalysis = SentimentAnalysis()
    #text_path = join("extracted_audio",audio)
    try:
        sentimentAnalysis.append(thread_sentimentAnalysis.analyseSentiment(text))
    except Exception as e:
        print(f"Error sentiment analysis audio from {text}: {e}")

print(sentimentAnalysis)

translatedText = []
#Serially translating text to spanish
for text in transcribedAudio:
    thread_translatingText = SpanishTranslator()
    try:
        translatedText.append(thread_translatingText.translate(text))
    except Exception as e:
        print(f"Error translating from {text}: {e}")

#Serially extracting emotions from text
for text in transcribedAudio:
    thread_emotionExtractor = EmotionExtractor()
    try:
        translatedText.append(thread_emotionExtractor.extractEmotions(text))
    except Exception as e:
        print(f"Error extracting emotions from {text}: {e}")