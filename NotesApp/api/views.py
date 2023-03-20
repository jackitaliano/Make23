from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import NoteSerializer, TakeNotesSerializer
from .models import Note
from .request_utils import summarize_transcript, transcribe_audio
from django.http import JsonResponse

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
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)
        
        transcript = serializer.data.get(self.transcript_key)
        notes = serializer.data.get(self.notes_key)
        
        return summarize_transcript(transcript, notes)

class AudioReceiverView(APIView):
    def post(self, request, *args, **kwargs):
        audio_file = request.FILES['audio_file']
        blob = audio_file.read()
        audio_fp = 'audio.webm'
        
        with open(audio_fp, 'wb') as f:
            f.write(blob)
            
        return transcribe_audio(audio_fp)
            
            
