from fastapi import FastAPI, Response
from fastapi.responses import FileResponse
import wave
import os

#import numpy as np
import torch
#from scipy.io.wavfile import read

#from preprocessing import preprocess_audio_dataset_for_tts
from pydantic_models import ProcessingData

import sys
sys.path.insert(0,"tortoise-tts")
import tortoise.api as api

GENERATED_RESULT_PATH = 'results'

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
async def generate_audio(data: ProcessingData):

    text_data = data.text_sentence
    audio_list_of_data = data.audio_data
    audio_data = [ torch.Tensor(i) for i in audio_list_of_data ]
    voice_name = data.voice_name
    preset = data.preset
    fast_mode = data.fast_mode

    if fast_mode:
        
        # get the last already generated file for particular voice
        output_file_name = ''
        files = [os.path.join(r,file) for r,d,f in os.walk(GENERATED_RESULT_PATH) for file in f]       
        
        if voice_name:
            files = [f for f in files if voice_name in f]

        # ['results\\custom_0_0.wav', 'results\\custom_0_1.wav', 'results\\custom_0_2.wav']
        
        output_file_name = files[-1]
        #output_full_file_name = os.path.join(GENERATED_RESULT_PATH, output_file_name)

        #result = wave.open(output_file_name, 'r')
        #result = read(output_file_name)

        return FileResponse(output_file_name, media_type="audio/wav")
    
    else:
        
        # send request to Tortoise-TTS to generate the new audio file
        #clips_paths  = preprocess_audio_dataset_for_tts(audio_data_folder, voice_name)

        tts = api.TextToSpeech()
        pcm_audio = tts.tts_with_preset(text_data, voice_samples=audio_data, preset=preset, k=1)
        result = pcm_audio

        return Response(content=result, media_type="audio/wav")
