from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import NoteSerializer, TakeNotesSerializer, NoteIdSerializer
from .models import Note
from .request_utils import summarize_request, transcribe_request, get_note_by_id
import json

with open("./api/api_keys.json", "r") as file:
    keys = json.load(file)
    open_ai_key = keys['open-ai']

class NoteView(generics.ListAPIView):
    serializer_class = NoteIdSerializer
    
    def get(self, request, format=None):
        note_id = request.GET.get('note_id')
        note = get_note_by_id(note_id)
        
        return Response(NoteSerializer(note).data, status=status.HTTP_200_OK)
    
class CreateNoteView(APIView):
    def post(self, request, format=None):
        note = Note(transcript="", note_buffer="", notes="")
        note.save()
        
        return Response(NoteSerializer(note).data, status=status.HTTP_201_CREATED)
        
        
class TakeNotesView(APIView):
    # serializer_class = NoteIdSerializer
    
    def post(self, request, format=None):
        # serializer = self.serializer_class(data=request.data)
        # if not serializer.is_valid():
        #     return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)
        
        note_id = request.POST.get("note_id")
        print("id:", note_id)
        note = get_note_by_id(note_id)
        
        return summarize_request(open_ai_key, note)


class AudioReceiverView(APIView):
    
    def post(self, request, *args, **kwargs):
        note_id = request.POST.get('note_id')
        audio_file = request.FILES.get('audio_file')
 
        note = get_note_by_id(note_id)
        blob = audio_file.read()
        
        return transcribe_request(open_ai_key, note, blob)
            
            
