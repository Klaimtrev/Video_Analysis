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
                audio = recognizer.record(source, duration=180)
            # Transcribe audio to text using Google Web Speech API
            text = recognizer.recognize_google(audio)
            text_path = os.path.join(self.output_folder, self.replaceWAVtoTXT(name))
            with open(text_path, 'w') as file:
                file.write(text)
            print(f'Text has been written to {text_path}')
            listOfPaths.append(text_path)
            return text_path
        except Exception as e:
            # Catch any other exceptions and log them
            print(f"An error occurred: {e} Name of the file {audio_file}")