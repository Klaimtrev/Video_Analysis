# Big Data Analytics 2024 Project 1
# Technical Report

## Summary

The project demonstrates a systematic approach to processing videos through various stages including downloading, extracting audio, transcription, sentiment analysis, translation, and emotion detection. Each stage is supported by a dedicated Python class, leveraging libraries like moviepy, speech_recognition, TextBlob, googletrans, spaCy, nltk, and NRCLex to achieve the desired transformations and analyses.

To enhance efficiency and manage concurrent tasks, the project employs multithreading, a semaphore to limit concurrent downloads, and a mutex to ensure synchronized access to shared resources. This modular design and use of advanced programming techniques make the code more organized, understandable, and efficient.

## Table of Contents
- [Big Data Analytics 2024 Project 1](#big-data-analytics-2024-project-1)
- [Technical Report](#technical-report)
  - [Summary](#summary)
  - [Table of Contents](#table-of-contents)
  - [Download\_URL](#download_url)
  - [Download\_Log](#download_log)
  - [Video\_Analysis](#video_analysis)
    - [Extract\_Audio](#extract_audio)
    - [Transcribe\_Audio](#transcribe_audio)
    - [Sentiment\_Analysis](#sentiment_analysis)
    - [Translate\_Text](#translate_text)
    - [Extract\_Emotions](#extract_emotions)

## Download_URL

First i used a sequential script to download each video from the urls I saved in [video_urls.txt](Video_Analysis\video_urls.txt).
The following code saves all the urls in a list:
```
url_list = []
with open("Video_Analysis/video_urls.txt", "r") as f:
    for line in f:
        url_list.append(line)
```
And then the following code calls the function to download a video where each video is passed.
```
for i in url_list:
    download_video(i)
```

However to use parallel programming, I decided to use threads instead of processes since downloading 15 videos do not require much processing power and they can be easily controlled with semaphores ,to limit the number of downloads that happen at the same time, and mutex, to restric access to download_log.txt and provent multiple threads from trying to write to it at the same time. Below you can see my implementation using a mutex and a semaphore:

```
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
```
This function also saves some extra information for another class called [Logger](Video_Analysis\logger.py), which I will explain later.
Finally this download_video function is called using a list where all the threads are saved and the threads are started later in another for loop:
```
## Parallel Download videos from the list
downloadThreads = []
for i in range(len(url_list)):
    thread = threading.Thread(target=download_video, args=(url_list[i],i,))
    downloadThreads.append(thread)
    thread.start()

# Wait for all threads to complete
for thread in downloadThreads:
    thread.join()
```
## Download_Log

I created a different class called [Logger](Video_Analysis\logger.py). It captures information about each downloaded video including: the video name, the thread that downloaded it, the timestamp of the download, the URL of the video, and whether the download was successful. It also saves all this information in a text file called [download_log.txt](Video_Analysis\download_log.txt)

As I explained in thre previous section I used a mutex that restricts the access of threads to the text file. The code of the logger class is very simple:
```
class Logger:
    def __init__(self,videoName, thread, timeStamp, URL, Downloaded):
        self.videoName = videoName
        self.thread = thread
        self.timeStamp = timeStamp
        self.URL = URL
        self.Downloaded = Downloaded

    def getData(self):
        return self.videoName,self.thread,self.timeStamp,self.URL,self.Downloaded
    
    def recordData(self):
        with open('download_log.txt', 'a') as file:
            file.write(f"Timestamp: {self.timeStamp} Name of video: {self.videoName} Download by thread #: {self.thread} URL: {self.URL} Download: {self.Downloaded}\n")
```

## Video_Analysis

Before all the scripts below I used a small for loop to get the path for each of the videos downloaded:
```
#check the videofiles
videofiles = [f for f in listdir('video_output') if isfile(join('video_output', f))]
```
I did this because I was getting some errorrs regarding the video paths.

### Extract_Audio

For most of the scripts in this section I created a paralell programming and sequential programming version.  
For example here is the sequential version to extract audio:
```
#Serially extract audio from the downloaded videos
for video in videofiles:
    audioExtractor = AudioExtractor()
    video_path = join("video_output", video)  # Ensure full path is passed
    try:
        audioExtracted.append(audioExtractor.extractAudio(video_path))
    except Exception as e:
        print(f"Error extracting audio from {video_path}: {e}")
```
In this version the AudioExtractor class is created for every videopath and once the function extractAudio finishes, it saves the path of the audio extracted inside a list called audioExtracted.

The asynchronous version is very similar to the sequential one, but instead of creating a new AudioExtractor for every video, I created a list of threads of AudioExtractor classes and used them to extract audio from the videos asynchronously.
```
#Parallel extract audio from the downloaded videos
for i in range(len(videofiles)):
    video_path = join("video_output", videofiles[i])  # Ensure full path is passed
    thread = threading.Thread(target=AudioExtractor().extractAudio, args=(video_path,audioExtracted,))
    audioExtractThreads.append(thread)
    thread.start()

# Wait for all threads to complete
for thread in audioExtractThreads:
    thread.join()
```
Here I realized that using thread.join is very important because even though I can initialize threads without it, it makes sure that the threads complete their tasks before running the next line of code. I also would like to mention that extracting the audio from video did not seem to be heavyweight for my machine so I decided to keep using threads instead of processses.

My class audioExtractor is very simple:
```
import moviepy.editor as mp
import os

class AudioExtractor:
    def __init__(self):
        self.output_folder = "extracted_audio"
        # Create the folder if it does not exist
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

    #replace the mp4 extension with wav
    def replaceMP4(self,str):
        return str[:-4] + '.wav' if str.endswith('.mp4') else str

    #Extract the audio from the video
    def extractAudio(self, videoPath,audioExtracted):
        video = mp.VideoFileClip(videoPath)
        name = video.filename
        name = os.path.basename(video.filename)  # Get the base name of the file
        audio_path = os.path.join(self.output_folder, self.replaceMP4(name))  # Create the path in the "extracted_audio" folder
        video.audio.write_audiofile(audio_path)
        audioExtracted.append(audio_path)
        return audio_path
```

In the constructor of the class I defined the folder where all the extracted audio will be saved, if it does not exists, it will create it.

Then, the method replaceMP4 replaces the extension of the name of the file with wav.

Finally the method to extract the Audio  uses the path of the video file to get the audio and it extracts it with the moviepy.editor library and the new path is saved in a list. This list will be used for other tasks.

The other classes are very similar to this one.

### Transcribe_Audio
The class audioTranscriber writes the text based on an audio file and saves the result in a folder. I got a lot of problems using the library needed for this since Google Web Speech API told me that there were some bad requests for some files but I fixed it by limiting the duration of the audio files to only 3 minutes. I used threats for this class as well since it relies in remote processing and not local processing power.
```
import speech_recognition as sr
import os

class AudioTranscriber():
    def __init__(self):
        self.output_folder = "transcribed_Text"
        # Create the folder if it does not exist
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

    def replaceWAVtoTXT(self, str):
        return str[:-4] + '.txt' if str.endswith('.wav') else str
    
    def transcribe(self, audio_file, listOfPaths):
        recognizer = sr.Recognizer()
        name = os.path.basename(audio_file)
        try:
            with sr.AudioFile(audio_file) as source:
                audio = recognizer.record(source)
            # Transcribe audio to text using Google Web Speech API
            text = recognizer.recognize_google(audio)
            text_path = os.path.join(self.output_folder, self.replaceWAVtoTXT(name))
            with open(text_path, 'w') as file:
                file.write(text)
            print(f'Text has been written to {text_path}')
            listOfPaths.append(text_path)
            return text_path
        except sr.RequestError as e:
            # API was unreachable or unresponsive
            print(f"Could not request results from Google Web Speech API; {e} Name of the file {audio_file}")
        except sr.UnknownValueError:
            # Speech was unintelligible
            print("Google Web Speech API could not understand audio")
```

The code is very similar to the previous class but this time instead of saving it as a .wav file it changes it to txt and uses the speech_recognition library to extract the text from the audio.

### Sentiment_Analysis
It performs sentiment analysis on text files. It reads text content from a file, analyzes the sentiment using the TextBlob library, and saves the sentiment results to a new file.
```
from textblob import TextBlob
import os

class SentimentAnalysis():

    def __init__(self):
        self.output_folder = "sentiment_analysis"
        # Create the folder if it does not exist
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

    def replaceTXTtoSentimentTXT(self, str):
        return str[:-4] + 'sentiment.txt' if str.endswith('.txt') else str
    

    def analyseSentiment(self,text_file):
        try:
            with open(text_file, "r") as file:
                content = file.read()
            blob = TextBlob(content)
            text_path = os.path.join(self.output_folder, self.replaceTXTtoSentimentTXT(os.path.basename(text_file)))
            with open(text_path, "w+") as f:
                f.write("Polarity = " + str(blob.sentiment.polarity) + " Subjectivity = " + str(blob.sentiment.subjectivity))
            print(f'Sentiment analysis saved to {text_path}')
            return text_path
        except FileNotFoundError as e:
            print(f"Error analyzing sentiment from {text_file}: {e}")

        #return text_path


```
### Translate_Text
In the translator file there is a SpanishTranslator class that uses the Google Translate API through the googletrans library. I tried to use TextBlob but it didnt work.
```
from textblob import TextBlob
#I got an error using textblob so I used googletrans instead
from googletrans import Translator
import os


class SpanishTranslator:
    def __init__(self):
        self.output_folder = "translated_text"
        # Create the folder if it does not exist
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

    def replaceTXTtoTranslatedTXT(self, str):
        return str[:-4] + '_translated.txt' if str.endswith('.txt') else str

    def translate(self, text_file):
        try:
            translator = Translator()
            with open(text_file, "r") as file:
                content = file.read()
            #blob = TextBlob(content)
            translated = translator.translate(content, src='en', dest='es')
            translated_text = translated.text
            text_path = os.path.join(self.output_folder, self.replaceTXTtoTranslatedTXT(os.path.basename(text_file)))
            with open(text_path, "w+") as f:
                f.write(translated_text)
            print(f'Translated text saved to {text_path}')
            return text_path
        except FileNotFoundError as e:
            print(f"Error translating text from {text_file}: {e}")
```
### Extract_Emotions
Finally my emotionExtractor class analyzes the emotions in a text file and save the results to a new file. This class uses libraries like spaCy for natural language processing, nltk for tokenization, and NRCLex for emotion detection. At the beginning of running the code it downloads the punkt package.
```
import spacy,nltk
import os
from nrclex import NRCLex
nlp = spacy.load('en_core_web_sm')
nltk.download('punkt')


class EmotionExtractor():
    def __init__(self):
        self.output_folder = "emotions_detected"
        # Create the folder if it does not exist
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

    def replaceTXTtoEmotionTXT(self, str):
        return str[:-4] + '_emotion.txt' if str.endswith('.txt') else str
    
    def extractEmotions(self, text_file):
        try:
            with open(text_file, "r") as file:
                content = file.read()
            doc = nlp(content)
            full_text = ' '.join([sent.text for sent in doc.sents])
            emotion = NRCLex(content)
            text_path = os.path.join(self.output_folder, self.replaceTXTtoEmotionTXT(os.path.basename(text_file)))
             # Convert the emotion frequencies to a formatted string
            emotion_frequencies_str = "\n".join([f"{emotion}: {frequency}" for emotion, frequency in emotion.affect_frequencies.items()])
            with open(text_path, "w+") as f:
                f.write("Detected Emotions and Frequencies:\n")
                f.write(emotion_frequencies_str)
            print(f'Emotions saved to {text_path}')
            return text_path
        except FileNotFoundError as e:
            print(f"Error extracting emotions from {text_file}: {e}")
```
