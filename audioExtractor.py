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
        return str[:-3] + '.wav' if str.endswith('.mp4') else str

    #Extract the audio from the video
    def extractAudio(self, videoPath):
        video = mp.VideoFileClip(videoPath)
        name = video.filename
        name = os.path.basename(video.filename)  # Get the base name of the file
        audio_path = os.path.join(self.output_folder, self.replaceMP4(name))  # Create the path in the "extracted_audio" folder
        video.audio.write_audiofile(audio_path)
        return audio_path