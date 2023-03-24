
from rest_framework.response import Response
from rest_framework import status
from .serializers import NoteSerializer
from .models import Note
from .utils import chat, transcribe
from rest_framework.response import Response

def summarize_request(api_key: str, note: Note):
    try:
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
        

def transcribe_request(api_key:str, note: Note, blob):
    if len(blob) < 10:
        return Response(status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
    
    audio_fp = 'audio.webm'
    write_blob_to_file(blob, audio_fp)
    
    try: 
        new_content = transcribe.transcribe(api_key, audio_fp)
        
        old_transcript = note.transcript 
        new_transcript = old_transcript + new_content
        note.transcript = new_transcript
        note.note_buffer += new_content
        note.save(update_fields=['transcript', 'note_buffer'])
        
        return Response(NoteSerializer(note).data, status=status.HTTP_200_OK)
        
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)
    
        
def get_note_by_id(id: str):
    queryset = Note.objects.filter(note_id=id)
    if queryset.exists():
        return queryset[0]
    
    print("New note created")
    return Note()

def write_blob_to_file(blob, fp):
    with open(fp, 'wb') as f:
            f.write(blob)
        