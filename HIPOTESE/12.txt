import os
from urllib.request import urlretrieve
import numpy as np
import matplotlib.pyplot as plt
import mne
from scipy.signal import butter, filtfilt

# ↓ Baixa EDF diretamente do PhysioNet ↓
url = "https://www.physionet.org/pn6/chbmit/chb01/chb01_01.edf"
local_file = "chb01_01.edf"
if not os.path.exists(local_file):
    print("Baixando dados EEG...")
    urlretrieve(url, local_file)
    print("Download concluído.")

# Carrega o arquivo EDF (primeiro canal)
raw = mne.io.read_raw_edf(local_file, preload=True, verbose=False)
data, times = raw[:1]  # canal 0

# Preprocessamento: filtro banda 1–50 Hz
def bandpass_filter(sig, low=1, high=50, fs=256):
    b, a = butter(2, [low/(fs/2), high/(fs/2)], btype='band')
    return filtfilt(b, a, sig)

sinal = data[0]
sinal_f = bandpass_filter(sinal, fs=raw.info['sfreq'])

# Quantização em símbolos
def quantizar_sinal(sinal, n_niveis=4):
    min_val, max_val = sinal.min(), sinal.max()
    bins = np.linspace(min_val, max_val, n_niveis + 1)
    s = np.digitize(sinal, bins) - 1
    s[s == n_niveis] = n_niveis - 1
    return s

fita = quantizar_sinal(sinal_f)

# Plot do canal e fita
plt.figure(figsize=(12,5))
plt.subplot(2,1,1)
plt.plot(times, sinal_f)
plt.title("EEG Real – Canal 0")
plt.subplot(2,1,2)
plt.imshow([fita], aspect='auto', cmap='tab20', extent=[times.min(), times.max(), 0, 1])
plt.yticks([])
plt.title("Fita vetorial quantizada")
plt.xlabel("Tempo (s)")
plt.tight_layout()
plt.show()

# Limpa o arquivo EDF se quiser
# os.remove(local_file)
