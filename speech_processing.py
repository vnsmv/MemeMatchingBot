import librosa
import matplotlib.pyplot as plt
import librosa.display
from scipy.signal import find_peaks

def process_voice(file_info):
    downloaded_file = bot.download_file(file_info.file_path)
    filename = str(uuid.uuid4())
    file_name_full = "./voice/"+filename+".ogg"
    file_name_full_wav = "./voice/"+filename+".wav"
    with open(file_name_full, 'wb') as new_file:
        new_file.write(downloaded_file)

    file = AudioSegment.from_ogg(Path(file_name_full))
    file.export(file_name_full_wav, format = 'wav')
    os.remove(file_name_full)


def speech_metrics(username,file_path):
    y, sr = librosa.load(file_path, mono=True, duration=30)
    rms = librosa.feature.rms(y=y)
    chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
    spec_cent = librosa.feature.spectral_centroid(y=y, sr=sr)
    spec_bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)
    rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
    zcr = librosa.feature.zero_crossing_rate(y)
    mfcc = librosa.feature.mfcc(y = y, sr = sr)
    to_append = f'{username} {chroma_stft.mean()} {rms.mean()} {spec_cent.mean()} {spec_bw.mean()} {rolloff.mean()} {zcr.mean()}'
    for e in mfcc:
        to_append += f' {e.mean()}'

    return to_append
