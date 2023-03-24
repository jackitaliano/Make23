
from rest_framework.response import Response
from rest_framework import status
from .serializers import NoteSerializer
from .models import Note
from .utils import chat, transcribe
from rest_framework.response import Response

def summarize_request(api_key: str, transcript:str, notes:str):
    queryset = Note.objects.all()
        
    if queryset.exists():
        try:
            note = queryset[0]
            note_buffer = note.note_buffer
            notes = note.notes
            summarized = chat.summarize(api_key, notes, note_buffer)
            
            note.note_buffer = ""
            note.notes = summarized
            
            note.save(update_fields=['note_buffer', 'notes'])
            return Response(NoteSerializer(note).data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)
        
    else:
        summarized = chat.summarize(api_key, notes, transcript)
        note = Note(transcript=transcript, notes=notes)
        note.save()
        return Response(NoteSerializer(note).data, status=status.HTTP_201_CREATED)

def transcribe_request(api_key:str, audio_fp: str):
    queryset = Note.objects.all()
    
    try: 
        new_content = transcribe.transcribe(api_key, audio_fp)
        
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)
    
    if queryset.exists():
        note = queryset[0]
        old_transcript = note.transcript 
        new_transcript = old_transcript + new_content
        note.transcript = new_transcript
        note.note_buffer += new_content
        # note.transcript = new_content
        note.save(update_fields=['transcript', 'note_buffer'])
        
        return Response(NoteSerializer(note).data, status=status.HTTP_200_OK)
    
    else:
        note = Note(transcript=new_content, note_buffer=new_content, notes="")
        note.save()
        return Response(NoteSerializer(note).data, status=status.HTTP_201_CREATED)
        
        