from fastapi import FastAPI, Response
import wave
from TTS import api

#from app.preprocessing import preprocess_audio_dataset_for_tts
from app.pydantic_models import ProcessingData

GENERATED_RESULT_PATH = 'D:\it-academy\data science\practice\Graduation Project\Tortoise TTS demo\tortoise-tts\results'

# Calls TTS with one of a set of preset generation parameters. Options:
# 'ultra_fast': Produces speech at a speed which belies the name of this repo. (Not really, but it's definitely fastest).
# 'fast': Decent quality speech at a decent inference rate. A good choice for mass inference.
# 'standard': Very good quality. This is generally about as good as you are going to get.
# 'high_quality': Use if you want the absolute best. This is not really worth the compute, though.

# Initialize API Server
app = FastAPI(
    title = "Text-to-speech with voice cloning",
    version="0.0.1"
)

@app.get('/')
async def root():
	return {"server_started" : "Please send post request on /api/tts/ to syntetize audio"}

@app.post('/api/tts/')
async def generate_audio(body: ProcessingData):

    text_data = ProcessingData.text_sequence
    audio_data = ProcessingData.audio_data
	voice_name = ProcessingData.voice_name
	preset = ProcessingData.preset
    fast_mode = ProcessingData.fast_mode

    if fast_mode:
        
        # get the last already generated file for particular voice
        output_file_name = ''
        files = get_all_filenames_in_folder(GENERATED_RESULT_PATH)        
        
        if voice_name:
            files = [x for x in file if file.contains(voice_name)]

        output_file_name = files[-1]
        output_full_file_name = os.path.join(GENERATED_RESULT_PATH, output_file_name)

        result = wave.open(output_full_file_name, 'r')
    
    else:
        
        # send request to Tortoise-TTS to generate the new audio file
        #clips_paths  = preprocess_audio_dataset_for_tts(audio_data_folder, voice_name)
        #tts = api.TextToSpeech()
        pcm_audio = tts.tts_with_preset(text_data, voice_samples=audio_data, preset=preset, k=1)
        result = pcm_audio

    return Response(content=result, media_type="audio/wav")


# List all files in a directory using os.listdir
def get_all_filenames_in_folder(basepath):

    file_names = []
    for file in os.listdir(basepath):
        if os.path.isfile(os.path.join(basepath, file)):
            file_names.append(file)
    
    return file_names