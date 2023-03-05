import pyaudio
import wave
import openai
import os
import multiprocessing
import firebase_admin
from firebase_admin import db

def record_audio():
    openai.api_key = "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"

    cred = firebase_admin.credentials.Certificate("./makeOhioAdminSDK.json")
    app = firebase_admin.initialize_app(cred,{
        'databaseURL': 'https://makeohio2023-default-rtdb.firebaseio.com/'
    })

    form_1 = pyaudio.paInt16 # 16-bit resolution
    chans = 1 # 1 channel
    samp_rate = 44100 # 44.1kHz sampling rate
    chunk = 4096 # 2^12 samples for buffer
    record_secs = 5 # seconds to record
    dev_index = 2 # device index found by p.get_device_info_by_index(ii)
    wav_output_filename = 'test1.wav' # name of .wav file

    audio = pyaudio.PyAudio() # create pyaudio instantiation

    #create two shared memory values
    manager = multiprocessing.Manager()
    sharedBase = manager.Value(str, "")
    sharedNew = manager.Value(str, "")

    ref = db.reference("/")
    ref.set({
        "NewSentence": ""
    })

    while(True):

        # create pyaudio stream
        stream = audio.open(format = form_1,rate = samp_rate,channels = chans, \
                            input_device_index = dev_index,input = True, \
                            frames_per_buffer=chunk)

        print("started recording")
        frames = []

        # loop through stream and append audio chunks to frame array
        for ii in range(0,int((samp_rate/chunk)*record_secs)):
            data = stream.read(chunk)
            frames.append(data)

        print("finished recording")

        # stop the stream, close it, and terminate the pyaudio instantiation
        stream.stop_stream()
        stream.close()
        #audio.terminate()

        # save the audio frames as .wav file
        wavefile = wave.open(wav_output_filename,'wb')
        wavefile.setnchannels(chans)
        wavefile.setsampwidth(audio.get_sample_size(form_1))
        wavefile.setframerate(samp_rate)
        wavefile.writeframes(b''.join(frames))
        wavefile.close()

        #create parent and child process
        childPID = os.fork()
        if(childPID ==0):
            #child process
            audio_file = open("./test1.wav", "rb")
            transcript = openai.Audio.translate("whisper-1", audio_file)

            result = transcript["text"]
            splitResult = result.rsplit('.', 1)

            if len(splitResult) == 1:
                sharedNew.value += splitResult[0]
            else:
                sharedBase.value += sharedNew.value + splitResult[0] + "."
                sharedNew.value = splitResult[1]

            print(sharedBase.value)
            #add to database
            ref.update({
                "NewSentence": sharedBase.value
            })
            sharedBase.value = ""


            os._exit(0)

if __name__ == '__main__':
    record_audio()
