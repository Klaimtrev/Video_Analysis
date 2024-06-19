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

