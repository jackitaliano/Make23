from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import NoteSerializer, TakeNotesSerializer
from .models import Note
from .request_utils import summarize_request, transcribe_request
import json

with open("./api/api_keys.json", "r") as file:
    keys = json.load(file)
    open_ai_key = keys['open-ai']

class NoteView(generics.ListAPIView):
    serializer_class = NoteSerializer
    
    def get(self, request, format=None):
        queryset = Note.objects.all()
        
        if queryset.exists():
            note = queryset[0]
            return Response(NoteSerializer(note).data, status=status.HTTP_200_OK)
        else:
            note = Note()
            return Response(NoteSerializer(note).data, status=status.HTTP_201_CREATED)
        
        

class TakeNotesView(APIView):
    serializer_class = TakeNotesSerializer
    transcript_key="transcript"
    notes_key="notes"
    
    def post(self, request, format=None):
        # serializer = self.serializer_class(data=request.data)
        # print(serializer)
        # if not serializer.is_valid():
        #     return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)
        
        # transcript = serializer.data.get(self.transcript_key)
        # notes = serializer.data.get(self.notes_key)
        transcript = request.data.get('transcript')
        notes = request.data.get('notes')
        
        return summarize_request(open_ai_key, transcript, notes)


class AudioReceiverView(APIView):
    count = 0
    
    def post(self, request, *args, **kwargs):
        audio_file = request.FILES['audio_file']
        blob = audio_file.read()
        if len(blob) < 10:
            return Response(status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        
        audio_fp = f'audio{AudioReceiverView.count}.webm'
        AudioReceiverView.count += 1
        
        with open(audio_fp, 'wb') as f:
            f.write(blob)
            
        return transcribe_request(open_ai_key, audio_fp)
            
            
