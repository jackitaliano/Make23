import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import json
import chat
import search
import urllib.parse
import markdown
from html2markdown import convert

keys : dict
with open('./py/keys.json', 'r') as file:
    keys = json.load(file)
    
open_key = keys['openai']
bing_key = keys['bing']

cred = credentials.Certificate('makeohio2023-firebase-adminsdk-iyviq-6daa757964.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://makeohio2023-default-rtdb.firebaseio.com'
})

ref = db.reference('/')
sentence_ref = db.reference('NewSentence')

# Define a callback to handle changes to the data
def on_data_change(event):
    if event.event_type == "put":
        new_content = event.data
        if new_content and len(new_content.split()) > 5:
            context_ref = db.reference('SummarizedData')
            context = context_ref.get()
            
            if context:
                markdown_context = convert(context)
            else:
                markdown_context=""
            
            try:
                notes = chat.summarize(open_key, markdown_context, new_content)
                urls = search.search(open_key, bing_key, notes)
                
            except Exception as e:
                print(e)
                return
            
            html_notes = markdown.markdown(notes)

            update_notes(html_notes)
            # update_related_links(urls)
            # update_related_images(urls)
        
def update_notes(text: str):
    ref.update({
        "SummarizedData": urllib.parse.quote(text)
    })
    
def update_related_links(url: str):
    text = url['url'] + '~' + url['title']
    ref.set({
        "RelatedLinks": text
    })

def update_related_images(url: str):
    text = url['url'] + '~' + url['title']
    ref.set({
        "RelatedImages": text
    })
    

# Listen to changes in the "users" node
sentence_ref.listen(on_data_change)

