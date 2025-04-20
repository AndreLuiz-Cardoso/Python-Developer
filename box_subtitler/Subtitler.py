from openai import OpenAI
from dotenv import load_dotenv
from pydub import AudioSegment

def subtitler(selected_file, context):
    extention_file = selected_file.name.split(".")[1]
    audio = AudioSegment.from_file(file=selected_file, format=extention_file)

    audio.export("audio.mp3", format="mp3")

    load_dotenv()

    client = OpenAI()

    with open("audio.mp3", "rb") as document:
        transcript = client.audio.transcriptions.create(
            file=document,
            model="whisper-1",
            language="pt", response_format="srt", prompt=context)

    print(transcript)

    with open("subtitle.srt", "w", encoding="utf-8") as document_subtitle:
        document_subtitle.write(transcript)
    
    return transcript