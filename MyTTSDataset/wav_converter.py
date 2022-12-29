import librosa
import os

file_names = []
basepath = 'wavs'
for file in os.listdir(basepath):
	if os.path.isfile(os.path.join(basepath, file)):
		file_names.append(file)

for audio_file in file_names: # "wavs/ah-01.wav" #48KHz

	# with the same playback speed
	x, sr = librosa.load(audio_file, sr=44100)
	librosa.output.write_wav("Test1.wav", x, sr=22050, norm=False)
	print(f"File {audio_file} converted")