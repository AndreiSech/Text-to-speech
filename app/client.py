from TTS import api
from fastapi.testclient import TestClient
from app.server import app
from app.preprocessing import preprocess_audio_dataset_for_tts

AUDIO_FILES_FOLDER = 'd:/it-academy/data science/practice/Graduation Project/Tortoise TTS demo/tortoise-tts/tortoise/voices/'
TEST_SENTENSE = "I'm Andrew Huberman and I'm a professor of neurobiology and ophthalmology"
FAST_MODE = True
VOICE_NAME = "custom"
PRESET = 'fast'

client = TestClient(app)

def syntesize_new_audio():

	audio_data_folder = AUDIO_FILES_FOLDER
	clips_paths  = preprocess_audio_dataset_for_tts(audio_data_folder, voice_name)

    response = client.post(
        "/api/tts/",
        headers = {"X-Token": "hailhydra"},
        json = {"text_sequence": text_data, 
				"audio_data": clips_paths,
				"voice_name": VOICE_NAME,
				"preset" : preset,
				"fast_mode": FAST_MODE},
    )
	print(response.status_code) # 201 if ok
	return response

if __name__ == "__main__":

    generated_audio = syntesize_new_audio(AUDIO_FILES_FOLDER)
	print(generated_audio)
	