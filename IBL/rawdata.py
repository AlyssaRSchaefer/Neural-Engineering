from one.api import ONE
from brainbox.io.spikeglx import Streamer
import matplotlib.pyplot as plt

one = ONE()

pid = '05ccc92c-fcb0-4e92-84d3-de033890c7a8'

t0 = 100 # timepoint in recording to stream
band = 'lf' # either 'ap' or 'lf'

sr = Streamer(pid=pid, one=one, remove_cached=False, typ=band)
first, last = (int(t0 * sr.fs), int((t0 + 1) * sr.fs))

# Important: remove sync channel from raw data, and transpose to get a [n_channels, n_samples] array
raw = sr[first:last, :-sr.nsync].T

# Plot LFP data
plt.figure(figsize=(10, 5))
#plt.plot(raw)
plt.title('Local Field Potential (LFP) Data')
plt.xlabel('Sample')
plt.ylabel('Amplitude')
plt.grid(True)
plt.psd(raw,NFFT=512,Fs=1000)
plt.xlim(0,100)
plt.show()
