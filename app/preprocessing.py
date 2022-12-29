import librosa
import os
import shutil
from scipy.io.wavfile import read
import numpy as np
import torch
#from TTS import utils

AUDIO_FILES_FOLDER_BASE = 'voices'
SAMPLES_TO_CONSIDER = 22050
SAMPLE_RATE = 22050

def preprocess_audio_dataset_for_tts(audio_folder, voice_name='custom'):
    
    clips_paths = os.path.join(audio_folder,voice_name)
    
    # copy *.wavs from audio_folder to clips_paths folder (if audio placed in external location)
    if audio_folder != AUDIO_FILES_FOLDER_BASE:
        copy_files(audio_folder, clips_paths)

    files = [os.path.join(r,file) for r,d,f in os.walk(clips_paths) for file in f]

    reference_clips = [load_audio(f, SAMPLE_RATE) for f in files]
    return reference_clips


def preprocess_audio_dataset(audio_folder=AUDIO_FILES_FOLDER_BASE):
    """Extracts MFCCs from music dataset and return them
    """

    # dictionary where we'll store MFCCs
    audio_data = []

    # loop through all sub-dirs
    for i, (dirpath, dirnames, filenames) in enumerate(os.walk(dataset_path)):

        # ensure we're at sub-folder level
        if dirpath is not dataset_path:

            # process all audio files in sub-dir and store MFCCs
            for f in filenames:
                file_path = os.path.join(dirpath, f)

                # load audio file and slice it to ensure length consistency among different files
                signal, sample_rate = librosa.load(file_path)

                # drop audio files with less than pre-decided number of samples
                if len(signal) >= SAMPLES_TO_CONSIDER:

                    # ensure consistency of the length of the signal
                    signal = signal[:SAMPLES_TO_CONSIDER]

                    # extract MFCCs
                    MFCCs = librosa.feature.mfcc(signal, SAMPLE_RATE, n_mfcc=num_mfcc, n_fft=n_fft,
                                                 hop_length=hop_length)

                    # store data for analysed track
                    audio_data.append(MFCCs.T.tolist())

    return audio_data


def load_audio(audiopath, sampling_rate):

    if audiopath[-4:] == '.wav':
        audio, lsr = load_wav_to_torch(audiopath)
    elif audiopath[-4:] == '.mp3':
        audio, lsr = librosa.load(audiopath, sr=sampling_rate)
        audio = torch.FloatTensor(audio)
    else:
        assert False, f"Unsupported audio format provided: { audiopath[-4:] }. Full name { audiopath }"

    # Remove any channel data.
    if len(audio.shape) > 1:
        if audio.shape[0] < 5:
            audio = audio[0]
        else:
            assert audio.shape[1] < 5
            audio = audio[:, 0]

    if lsr != sampling_rate:
        audio = torchaudio.functional.resample(audio, lsr, sampling_rate)

    # Check some assumptions about audio range. This should be automatically fixed in load_wav_to_torch, but might not be in some edge cases, where we should squawk.
    # '2' is arbitrarily chosen since it seems like audio will often "overdrive" the [-1,1] bounds.
    if torch.any(audio > 2) or not torch.any(audio < 0):
        print(f"Error with {audiopath}. Max={audio.max()} min={audio.min()}")
    audio.clip_(-1, 1)

    return audio.unsqueeze(0)


def load_wav_to_torch(full_path):
    sampling_rate, data = read(full_path)
    if data.dtype == np.int32:
        norm_fix = 2 ** 31
    elif data.dtype == np.int16:
        norm_fix = 2 ** 15
    elif data.dtype == np.float16 or data.dtype == np.float32:
        norm_fix = 1.
    else:
        raise NotImplemented(f"Provided data dtype not supported: {data.dtype}")
    return (torch.FloatTensor(data.astype(np.float32)) / norm_fix, sampling_rate)


def copy_files(source_directory, destination_directory):

    # getting all the files in the source directory
    files = os.listdir(source_directory)

    # copy all files
    shutil.copytree(source_directory, destination_directory, dirs_exist_ok=True)


if __name__ == "__main__":

    data = preprocess_audio_dataset_for_tts(AUDIO_FILES_FOLDER)
    print(data)