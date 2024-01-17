import ffmpeg
from openai import OpenAI

client = OpenAI()

class MediaHandler:
    def __init__(self):
        pass


    def extract_audio(self, input=None, output=None):
        ffmpeg.input(input).output(output, vn=True, filter='atempo=2.0', ab=64, acodec='libmp3lame').run()


    def compress_audio(self, input=None, output=None):
        ffmpeg.input(input).output(output, filter='atempo=2.0', ab=64, acodec='libmp3lame').run()


    def speech_to_text(self, audio_path=None):

        with open(audio_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="text"
            )
        return transcript


    def meeting_minutes(self, transcription):
        abstract_summary = self.abstract_summary_extraction(transcription)
        action_items = self.action_item_extraction(transcription)
        return {
            'abstract_summary': abstract_summary,
            'action_items': action_items,
        }


    def abstract_summary_extraction(transcription):
        response = client.chat.completions.create(
            model="gpt-4",
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
        return response['choices'][0]['message']['content']


    def action_item_extraction(transcription):
        response = client.chat.completions.create(
            model="gpt-4",
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
        return response['choices'][0]['message']['content']
