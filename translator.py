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