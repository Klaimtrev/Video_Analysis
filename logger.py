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
            file.write(f"Name of video: {self.videoName} thread #: {self.thread} Time: {self.timeStamp} URL: {self.URL}\n")



