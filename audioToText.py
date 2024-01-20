from openai import OpenAI
import os
from dotenv import load_dotenv

def generateNoCaption(filename):
    load_dotenv()
    client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'),)

    with open(os.path.join(os.path.dirname(__file__), f"audio/{filename}"), "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file, 
        response_format="verbose_json"
    )

    extracted_data = [{'start': item['start'], 'duration': item['end'] - item['start'], 'text': item['text'].strip()} for item in transcript.segments]
    return extracted_data
