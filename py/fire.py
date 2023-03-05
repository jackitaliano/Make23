import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import json
import chat
import search

# keys : dict
# with open('./keys.json', 'r') as file:
#     keys = json.load(file)
    
open_key = "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"
bing_key = "22898e58ec7b42df95d4a7b7de95c4cf"

cred = credentials.Certificate('makeohio2023-firebase-adminsdk-iyviq-6daa757964.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://makeohio2023-default-rtdb.firebaseio.com'
})

notes_ref = db.reference('SummarizedData')

# Define a callback to handle changes to the data
def on_data_change(event):
    if event.event_type == "put":
        new_content = event.data
        notes = chat.summarize(open_key, "", new_content)
        urls = search.search(open_key, bing_key, notes)
        
        print(notes)
        update_notes(notes)
        
def update_notes(text: str):
    notes_ref.set(text);

# Listen to changes in the "users" node
sentence_ref = db.reference('NewSentence')
sentence_ref.listen(on_data_change)

