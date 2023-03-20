import openai
import tempfile

def transcribe(api_key, audio_file_path):
    openai.api_key = api_key
    
    try:
        with open(audio_file_path, 'rb') as file:
            response = openai.Audio.translate("whisper-1", file)
            transcript = response['text']
    except Exception as e:
        print(e)
        return ""
        
    return transcript
        
