# Smart Notes
## Synopsis
Smart Notes records, transcribes, and takes notes on your lectures using the power of OpenAI's GPT-3.5turbo model and Whisper speech recognition. This system allows users to set aside notes during the lecture, and actually absorb the content without fear of missing key things to write down. New possibilities are open for the future of education, and we are taking full advantage.

## Motivation
Our team was participating in Make OH/IO, a 24 hour hack-a-thon, and wanted to create something entirely new using the technologies that had released just days before. We wanted something that could help everyone in the learning environment. For most students, this tool will simply allow them to pay more attention in class and go back over their notes for a greater understanding later. For some students, this tool is life changing. Students with learning disabilaties, difficulties with attention, or any number of other issues can prevent taking good notes while truly absorbing the lecture content. Smart Notes solves some of these issues, and attempts to even the educational playing field.

## Future Plans
### The Note Taking Experience
We are currently working on the following features to flesh out SmartNotes and to get a product to users as quickly as possible:
1. Develop a fully functional note-taking app with the added features of SmartNotes
2. Add personal tutor assistant trained on the knowledge base of the user's notes
3. Add support for generation of study guides, note-cards, etc. based on the content of the user's notes

### The Collaborative Experience
Going forward, we plan to develop the app into a collaborative platform where users can share notes, study guides, etc. The knowledge base of the collaborative platform would be immense and entirely based on real lectures from college courses across the country. With this kind of information, we're not only enhancing the note-taking experience, but setting up a platform to democratize higher education.

## Startup process
Terminal 1:
- cd ./NotesApp/frontend
- npm run dev

Terminal 2:
- cd ./NotesApp
- python manage.py runserver


*Note: In the future we will host this web-app and provide alternative options to the current (relatively expensive) Whisper API, so that anyone can use it*

## Dependencies
- pip install -r requirements
- npm install (a bunch of things that I'll put here later)
- openai api key (create file "api_keys.json" with entry {"openai": "your_key"})
 - due to cost, we currently can't leave a default key in for you
