from ast import Return
from pytube import YouTube
import threading, time
from logger import Logger

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
for i in range(len(url_list)):
    threading.Thread(target=download_video, args=(url_list[i],i,)).start()


