from gradio_client import Client
import requests
from flask import Flask, render_template
import shutil
import requests
from bs4 import BeautifulSoup
import random

def move_audio_file(source_path, destination_path):
    try:
        shutil.move(source_path, destination_path)
        return True  # Return True if the move was successful
    except Exception as e:
        print(f"Error moving the audio file: {str(e)}")
        return False  # Return False if there was an error

client = Client("https://facebook-seamless-m4t.hf.space/")

# Define the URL of the page containing the quotes
url = 'https://www.goodreads.com/quotes'
response = requests.get(url)


if response.status_code == 200:
    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all the quote elements on the page
    quote_elements = soup.find_all(class_='quoteText')

    # Extract the text of each quote into a list
    quotes = [quote.contents[0].strip().replace('“', '').replace('”', '') for quote in quote_elements]

    # Select a random quote from the list
    random_quote = random.choice(quotes)

    # Print the randomly selected quote
    print(random_quote)
else:
    print(f"Failed to fetch quotes. Status code: {response.status_code}")

# Predict using the Gradio client
result = client.predict(
    "T2ST (Text to Speech translation)",
    "file",
    "https://github.com/gradio-app/gradio/raw/main/test/test_files/audio_sample.wav",
    "https://github.com/gradio-app/gradio/raw/main/test/test_files/audio_sample.wav",
    random_quote,
    "English",
    "English",
    api_name="/run"
)

# Set the source and destination paths for moving the audio file
source_path = result[0]
destination_path = 'static/audio/audio.wav'

# Move the audio file to the static/audio folder
if move_audio_file(source_path, destination_path):
    print("Audio file moved successfully!")
else:
    print("Failed to move the audio file.")

gradio_result = {
    'result': result,
    'audio': destination_path
}

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', gradio_result=gradio_result)

if __name__ == "__main__":
    app.run(debug=True)
