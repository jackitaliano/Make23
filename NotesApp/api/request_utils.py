
from rest_framework.response import Response
from rest_framework import status
from .serializers import NoteSerializer
from .models import Note
from .utils import chat, transcribe
from rest_framework.response import Response

def summarize_transcript(api_key: str, transcript: str, notes: str=""):
    queryset = Note.objects.all()
    
    try:
        summarized = chat.summarize(api_key, "", transcript)
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)
        
    if queryset.exists():
        note = queryset[0]
        note.transcript = transcript
        note.notes = summarized
        note.save(update_fields=['transcript', 'notes'])
        return Response(NoteSerializer(note).data, status=status.HTTP_200_OK)
        
    else:
        note = Note(transcript=transcript, notes=summarized)
        note.save()
        return Response(NoteSerializer(note).data, status=status.HTTP_201_CREATED)

def transcribe_audio(api_key:str, audio_fp: str):
    queryset = Note.objects.all()
    
    try: 
        transcript = transcribe.transcribe(api_key, audio_fp)
        
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)
    
    if queryset.exists():
        note = queryset[0]
        note.transcript = transcript
        note.save(update_fields=['transcript'])
        return Response(NoteSerializer(note).data, status=status.HTTP_200_OK)
    
    else:
        note = Note(transcript=transcript, notes="")
        note.save()
        return Response(NoteSerializer(note).data, status=status.HTTP_201_CREATED)
        
        