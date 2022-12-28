import librosa
import os
import shutil
from TTS import utils

AUDIO_FILES_FOLDER_BASE = 'd:/it-academy/data science/practice/Graduation Project/Tortoise TTS demo/tortoise-tts/tortoise/voices/'
SAMPLES_TO_CONSIDER = 22050 * 2
SAMPLE_RATE = 22050

def preprocess_audio_dataset_for_tts(audio_folder='', voice_name='custom'):
    
    clips_paths=os.join(AUDIO_FILES_FOLDER_BASE,voice_name)
    
    # copy *.wavs from audio_folder to clips_paths folder
    if audio_folder:
        copy_files(audio_folder, clips_paths)

    reference_clips = [utils.audio.load_audio(p, SAMPLE_RATE) for p in clips_paths]
    return reference_clips


def preprocess_audio_dataset(audio_folder=AUDIO_FILES_FOLDER):
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


def copy_files(source_directory, destination_directory):

    # getting all the files in the source directory
    files = os.listdir(source_directory)

    # copy all files
    shutil.copytree(source_directory, destination_directory)


if __name__ == "__main__":

    data = preprocess_audio_dataset_for_tts(AUDIO_FILES_FOLDER)
    print(data)