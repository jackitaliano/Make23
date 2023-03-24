from django.urls import path 
from .views import NoteView, TakeNotesView, AudioReceiverView, CreateNoteView

urlpatterns = [
    path('note', NoteView.as_view()),
    path('take-notes', TakeNotesView.as_view()),
    path('audio', AudioReceiverView.as_view()),
    path('create-note', CreateNoteView.as_view()),
]