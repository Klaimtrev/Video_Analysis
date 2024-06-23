import os

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



