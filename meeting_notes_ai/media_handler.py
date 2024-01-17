import uuid
import os
import ffmpeg
from pathlib import Path
from openai import OpenAI

client = OpenAI()

class MediaHandler:
    def __init__(self):
        pass


    def extract_audio(self, input=None, output=None):
        print("Extracting audio...", end="")
        stream = ffmpeg.input(input)
        stream = ffmpeg.output(stream, output, vn=True, filter='atempo=2.0', ab=64, acodec='libmp3lame')
        ffmpeg.run(stream, overwrite_output=True)
        print(" done!")
        return output


    def compress_audio(self, input=None, output=None):
        stream = ffmpeg.input(input)
        stream = ffmpeg.output(stream, output, filter='atempo=2.0', acodec='libmp3lame')
        ffmpeg.run(stream, overwrite_output=True)
        return output


    def speech_to_text(self, audio_path):
        audio_path_obj = Path(audio_path)
        output_path = audio_path_obj.stem + "_processed.mp3"
        output_path = self.compress_audio(audio_path, output_path)
        with open(output_path, 'rb') as audio_file:
            print("Transcribing audio...", end="")
            transcription = client.audio.transcriptions.create(model="whisper-1", file=audio_file)
            print(" done!")
        return transcription.text


    def meeting_minutes(self, transcription):
        print(transcription)
        print("Extracting meeting summary...", end="")
        abstract_summary = self.abstract_summary_extraction(transcription)
        print(" done!")
        print("Extracting action items...", end="")
        action_items = self.action_item_extraction(transcription)
        print(" done!")
        return {
            'abstract_summary': abstract_summary,
            'action_items': action_items,
        }


    def abstract_summary_extraction(self, transcription):
        response = client.chat.completions.create(
            model="gpt-4-1106-preview",
            temperature=0,
            messages=[
                {
                    "role": "system",
                    "content": "You are a highly skilled AI trained in language comprehension and summarization. I would like you to read the following text and summarize it into a concise abstract paragraph. Aim to retain the most important points, providing a coherent and readable summary that could help a person understand the main points of the discussion without needing to read the entire text. Please avoid unnecessary details or tangential points."
                },
                {
                    "role": "user",
                    "content": transcription
                }
            ]
        )
        return response.choices[0].message.content


    def action_item_extraction(self, transcription):
        response = client.chat.completions.create(
            model="gpt-4-1106-preview",
            temperature=0,
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI expert in analyzing conversations and extracting action items. Please review the text and identify any tasks, assignments, or actions that were agreed upon or mentioned as needing to be done. These could be tasks assigned to specific individuals, or general actions that the group has decided to take. Please list these action items clearly and concisely."
                },
                {
                    "role": "user",
                    "content": transcription
                }
            ]
        )
        return response.choices[0].message.content


    def audio_to_minutes(self, audio_file):
        transcription = self.speech_to_text(audio_file)
        return self.meeting_minutes(transcription)
