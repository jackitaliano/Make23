from django.db import models
import random
import string

def generate_unique_code():
    length = 8

    while True:
        note_id = ''.join(random.choices(string.ascii_uppercase, k=length))
        if Note.objects.filter(note_id=note_id).count() == 0:
            break

    return note_id

class Note(models.Model):
    note_id = models.CharField(max_length=8, default=generate_unique_code, unique=True)
    transcript = models.TextField(default='')
    notes = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)
    