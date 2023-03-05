import tkinter as tk
import pyaudio
import wave
import openai

openai.api_key = "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"

FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 10
WAVE_OUTPUT_FILENAME = "output.wav"

# Create a new window
window = tk.Tk()

# Set the window title
window.title("SmartNotes: Voice Activated Tutor")

# Set the window size
window.geometry("700x700")

# Define a function to execute when the button is clicked
def button_click():
    window.update()

    p = pyaudio.PyAudio()

    # Open a stream to record audio
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    # Initialize the buffer to store audio data
    frames = []

    # Record audio for a specified duration
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    window.update()

    # Stop and close the audio stream
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save the recorded audio to a WAV file
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    audio_file = open("./output.wav", "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)

    print(transcript['text'])
    text_widget.insert("3.0", "Question: " + transcript["text"] + "\n")
    window.update()

    preprompt = "You are a tutor bot. You will be asked questions related to academics and you will only answer when questioned."
    messages= [{"role": "system", "content": preprompt}]
    messages.append({"role": "user", "content": transcript["text"]})
    completion = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = messages
    )

    chat_response = completion.choices[0].message.content
    text_widget.insert("3.0", "Answer: " + chat_response)
    


# Create a Text widget
text_widget = tk.Text()
text_widget.insert('1.0', "This is a voice activated tutor. Please ask a question to get help with content!\n")

# Add the Text widget to the window

# Create a button widget
button = tk.Button(window, text="", command=button_click)

# Add the button to the window
button.pack()
text_widget.pack()

# Display the window
window.mainloop()

# Set the audio settings


# Initialize the PyAudio object