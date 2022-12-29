from fastapi.testclient import TestClient
from server import app
from preprocessing import preprocess_audio_dataset_for_tts
import torch
#from playsound import playsound
#import simpleaudio as sa
#from scipy.io.wavfile import write
from datetime import datetime
import os

AUDIO_FILES_FOLDER = 'voices'
TEXT_SENTENSE = "I'm Andrew Huberman and I'm a professor of neurobiology and ophthalmology"
FAST_MODE = False
VOICE_NAME = "custom"
PRESET = 'fast'
AUDIO_FROM_SERVER_FOLDER = 'audio'

client = TestClient(app)

def syntesize_new_audio():

	audio_data_folder = AUDIO_FILES_FOLDER
	voice_name = VOICE_NAME
	audio_tensors = preprocess_audio_dataset_for_tts(audio_data_folder, voice_name)
	#print(audio_tensors)

	# TypeError: Object of type Tensor is not JSON serializable => to numpy, but RuntimeError: Numpy is not available because librosa => to List
	clips_data  = [ t.tolist() for t in audio_tensors ]
	#print(clips_data)

	response = client.post(
        "/api/tts/",
        json = {"text_sentence": TEXT_SENTENSE, 
				"audio_data": clips_data,
				"voice_name": VOICE_NAME,
				"preset" : PRESET,
				"fast_mode": FAST_MODE},
    )
	print(f"Response status code: {response.status_code}") # 2xx if ok
	return response

#def play_sound(file_path="results/custom_0_0.wav"):
	#playsound('myfile.wav')
	
	#wave_obj = sa.WaveObject.from_wave_file(file_path)
	#play_obj = wave_obj.play()
	#play_obj.wait_done()

if __name__ == "__main__":
    
	generated_audio = syntesize_new_audio()
	wav_audio = generated_audio.content
	
	# store to disc to play
	dt = datetime.now()
	ts = datetime.timestamp(dt)
	name = f"{VOICE_NAME}-{ts}.wav"
	with open(os.path.join(AUDIO_FROM_SERVER_FOLDER,name), mode='bx') as f:
		f.write(wav_audio)

	#play_sound()