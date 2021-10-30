import librosa
import matplotlib.pyplot as plt
import librosa.display
from scipy.signal import find_peaks


audio_data = '1.wav'
y, sr = librosa.load(audio_data, mono=True, duration=30)

# Creare enpty CSV file

header = 'filename chroma_stft rms spectral_centroid spectral_bandwidth rolloff zero_crossing_rate'
for i in range(1, 21):
    header += f' mfcc{i}'
header += ' label'
header = header.split()

# Wr

file = open('dataset.csv', 'w', newline='')
with file:
    writer = csv.writer(file)
    writer.writerow(header)

rms = librosa.feature.rms(y=y)
chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
pec_cent = librosa.feature.spectral_centroid(y=y, sr=sr)
spec_bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)
rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
zcr = librosa.feature.zero_crossing_rate(y)
mfcc = librosa.feature.mfcc(y=y, sr=sr)

to_append = f'{audio_data} {np.mean(chroma_stft)} {np.mean(rms)} {np.mean(spec_cent)} {np.mean(spec_bw)} {np.mean(rolloff)} {np.mean(zcr)}'
for e in mfcc:
    to_append += f' {np.mean(e)}'
    # to_append += f' {g}'

print(to_append)
file = open('dataset.csv', 'a', newline='')
with file:
    writer = csv.writer(file)
    writer.writerow(to_append.split())




# peaks, _ = find_peaks(x, distance=20)
# X = librosa.stft(x)
# Xdb = librosa.amplitude_to_db(abs(X))

#plt.figure(figsize=(14, 5))

librosa.display.waveplot(y, sr=sr)
plt.show()
#print(Xdb)

#(94316,) 22050
