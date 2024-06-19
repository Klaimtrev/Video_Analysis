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