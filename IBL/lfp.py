from one.api import ONE
from brainbox.io.one import SpikeSortingLoader

one = ONE(base_url='https://openalyx.internationalbrainlab.org')
t0 = 100 # timepoint in recording to stream

pid = 'da8dfec1-d265-44e8-84ce-6ae9c109b8bd'
ssl = SpikeSortingLoader(pid=pid, one=one)
# The channels information is contained in a dict table / dataframe
channels = ssl.load_channels()

# Get AP and LFP spikeglx.Reader objects
sr_lf = ssl.raw_electrophysiology(band="lf", stream=True) # THIS LINE DOES NOT WORK
sr_ap = ssl.raw_electrophysiology(band="ap", stream=True) # SSL HAS NO ATTRIBUTE WITH THIS NAME