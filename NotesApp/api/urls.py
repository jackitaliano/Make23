from django.urls import path 
from .views import NoteView, TakeNotesView, AudioReceiverView

urlpatterns = [
    path('note', NoteView.as_view()),
    path('take-notes', TakeNotesView.as_view()),
    path('audio', AudioReceiverView.as_view()),
]