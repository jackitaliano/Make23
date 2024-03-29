from rest_framework import serializers
from .models import Note

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ('note_id', 'transcript', 'notes', 'note_buffer', 'created_at')

class TakeNotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ('transcript', 'notes')
        
class NoteIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ('note_id')