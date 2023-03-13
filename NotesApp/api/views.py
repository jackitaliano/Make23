from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import NoteSerializer, TakeNotesSerializer
from .models import Note
from .utils import chat

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
        
        queryset = Note.objects.all()
        transcript = serializer.data.get(self.transcript_key)
        notes = serializer.data.get(self.notes_key)
        
        summarized = chat.summarize("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", "", transcript)
        
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
            


        