from ast import Return
from pytube import YouTube
import threading, time
from logger import Logger
from audioExtractor import AudioExtractor
from audioTranscriber import AudioTranscriber
from sentimentAnalyser import SentimentAnalysis

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
    current_timestamp = time.time()
    thread_log = Logger(yt.title,index,current_timestamp,url,"Completed")
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

## Serially Download videos from the list

#for i in url_list:
#    download_video(i)

## Parallel Download videos from the list
downloadThreads = []
for i in range(len(url_list)):
    thread = threading.Thread(target=download_video, args=(url_list[i],i,))
    downloadThreads.append(thread)
    thread.start()
    #AudioExtractor(url_list[i])


# Wait for all threads to complete
for thread in downloadThreads:
    thread.join()

#check the videofiles
videofiles = [f for f in listdir('video_output') if isfile(join('video_output', f))]
audioExtracted = []

#Serially extract audio from the downloaded videos
for video in videofiles:
    thread_audioExtractor = AudioExtractor()
    video_path = join("video_output", video)  # Ensure full path is passed
    try:
        audioExtracted.append(thread_audioExtractor.extractAudio(video_path))
    except Exception as e:
        print(f"Error extracting audio from {video_path}: {e}")

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
