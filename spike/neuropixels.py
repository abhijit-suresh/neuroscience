import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import platform
import scipy.stats as stats
import seaborn as sns
import signal as signal

from allensdk.brain_observatory.ecephys.ecephys_project_cache import EcephysProjectCache
from allensdk.brain_observatory.ecephys import ecephys_session

cache = EcephysProjectCache.fixed(manifest=manifest_path)

"""
Neuropixels dataset from the Allen Institute
"""

# Load data.
platstring = platform.platform()

if "Darwin" in platstring:
    # OS X 
    data_root = "/Volumes/Brain2019/"
elif "Windows"  in platstring:
    # Windows (replace with the drive letter of USB drive)
    data_root = "E:/"
elif ("amzn1" in platstring):
    # then on AWS
    data_root = "/data/"
else:
    # then your own linux platform
    # EDIT location where you mounted hard drive
    data_root = "/media/$USERNAME/Brain2019/"

manifest_path = os.path.join(data_root, "dynamic-brain-workshop/visual_coding_neuropixels/2019/manifest.json")

# Get information.
sessions = cache.get_sessions()
sessions.head()

# Recordings across visual areas
cache = EcephysProjectCache.fixed(manifest=manifest_path)
sessions = cache.get_sessions()
vis_areas = ["VISp","VISl","VISal","VISrl","VISam","VISpm"]
vis_session_list = []
for session_id in sessions.index:
    session_areas = sessions.structure_acronyms.loc[session_id]
    vis_areas_in_session = [area for area in vis_areas if area in session_areas]
    if len(vis_areas_in_session)==6:
        vis_session_list.append(session_id)
print(vis_session_list)
session_id = vis_session_list[0]
session = cache.get_session_data(session_id)

# Visualize.
for i, area in enumerate(vis_areas):
    vis_unit_list = session.units[session.units.structure_acronym==area].index
    for i,unit in enumerate(vis_unit_list[:20]):
        spike_times =  session.spike_times[unit]                       
        plt.plot(spike_times, np.repeat(i, len(spike_times)), "|", color="gray") 
    plt.title(area) 
    plt.xlim(0,300)
    plt.show()

# Inter-spike interval distribution (ISI distribution)
unit_id = session.units.index.values[0]
unit_spikes = session.spike_times[unit_id]
isi = np.diff(unit_spikes)
isi = isi*1000 # convert to ms
print(isi[:20])

# Visualize.
fig,ax = plt.subplots(1,2,figsize=(10,4),sharey=True)
ax[0].hist(isi,bins=200,range=(0,200))
ax[1].hist(isi,bins=20,range=(0,20))
plt.ylabel("Count")
plt.xlabel("Inter-spike interval (ms)")
plt.show()

# Show in chart.
snr_df = session.units.sort_values(by=["snr"], ascending=False)
snr_df.head()

# Get spike times for 50 units with highest SNR.
unit_list = snr_df.index.values[:50]

# Figure setup
fig,ax = plt.subplots(5,10,figsize=(15,7),sharex=True)
ax = ax.ravel()

# Plot ISI distribution for each unit.
for i,unit in enumerate(unit_list):
    unit_spikes = session.spike_times[unit]
    if len(unit_spikes) > 3000:
        isi = np.diff(unit_spikes)
        ax[i].hist(isi,bins=50,range=(0,0.3))
        ax[i].set_title(str(unit_list[i]),fontsize=7)

plt.xlim(0,0.3)
for i in ax:
    i.axis("off")

# Explore responses to natural scenes.
stim_table = session.get_presentations_for_stimulus("natural_scenes")
stim_ids = stim_table.index.values
frames = session.get_stimulus_parameter_values(stimulus_presentation_ids=stim_ids, drop_nulls=False)["frame"]
frames = np.sort(frames)
frames

# Calculate spikes in 5 ms bins.
stim_presentation_ids = stim_table[stim_table.frame==46].index.values
bin_width = 0.005
duration = stim_table.duration.mean()
pre_time = -duration
post_time = 2*duration
bins = np.arange(pre_time, post_time+bin_width, bin_width)   
histograms = session.presentationwise_spike_counts(
    bin_edges=bins,
    stimulus_presentation_ids=stim_presentation_ids,
    unit_ids=None
)
mean_histograms = histograms.mean(dim="stimulus_presentation_id")
rates = mean_histograms/bin_width

# Plot the peristimulus time histogram (PSTH).
def plot_psth(unit_id, rates, ax=None, title=None):
    #Default params
    if not ax:
        fig,ax = plt.subplots(1,1,figsize=(6,3))
    rates.loc[{"unit_id":unit_id}].plot(ax=ax)
    ax.axvspan(0, duration, color="gray", alpha=0.1)
    ax.set_ylabel("Firing rate (spikes/second)")
    ax.set_xlabel("Time (s)")
    ax.set_xlim(pre_time,post_time)
    if ax:
        ax.set_title(title)
        ax.set_xlabel("")
        ax.set_ylabel("")

unit_id = 914686471 #unit_list[0]
plot_psth(unit_id, rates)

unit_id = 914686471
fig,ax = plt.subplots(15, 8, figsize=(18,20), sharex=True, sharey=True)
ax = ax.ravel()

# Calculate histograms for all presentations at once - this may take a minute.
histograms = session.presentationwise_spike_counts(
    bin_edges=bins,
    stimulus_presentation_ids=stim_table.index.values,
    unit_ids=None
    )

for i,frame in enumerate(frames):
    stim_presentation_ids = stim_table[stim_table.frame==frame].index.values
    # Select the histograms for this frame and average.
    frame_histograms = histograms.loc[{"stimulus_presentation_id":stim_presentation_ids}]
    mean_histograms = frame_histograms.mean(dim="stimulus_presentation_id")
    rates = mean_histograms/bin_width
    
    plot_psth(unit_id, rates, ax=ax[i], title=frame)
plt.tight_layout()

# Plot the image that shows the largest response for this unit.
plt.imshow(cache.get_natural_scene_template(105), cmap="gray")

# Responses to natural scenes
spike_stats = session.conditionwise_spike_statistics(stimulus_presentation_ids=stim_ids, unit_ids=unit_list)
spike_stats.head()

unit_id = 914686471
response_mean = np.empty((len(frames)))
response_sem = np.empty((len(frames)))
for i,frame in enumerate(frames):
    stim_id = stim_table[stim_table.frame==frame].stimulus_condition_id.iloc[0]
    response_mean[i] = spike_stats.loc[(unit_id, stim_id)].spike_mean
    response_sem[i] = spike_stats.loc[(unit_id, stim_id)].spike_sem
plt.errorbar(range(118), response_mean[1:], yerr=response_sem[1:], fmt="o")
plt.axhspan(response_mean[0]+response_sem[0], response_mean[0]-response_sem[0], color="gray", alpha=0.3)
plt.axhline(y=response_mean[0], color="gray", ls="--")

# Responses to natural scenes
response_norm = response_mean - response_mean[0]
N = float(len(response_norm))
ls = ((1-(1/N) * ((np.power(response_norm.sum(),2)) / (np.power(response_norm,2).sum()))) / (1-(1/N)))
print(ls)

# Population correlations and cross-correlograms of spiking activity
drift = session.get_presentations_for_stimulus("drifting_gratings")

# Get the info about the drifting gratings session.
first_drift_id = drift.index.values[0]
first_drift_duration = drift.loc[first_drift_id, "stop_time"] - drift.loc[first_drift_id, "start_time"]

# Construct the time domain at 10 ms resolution.
time_step = 1 / 100
time_domain = np.arange(0.0, first_drift_duration + time_step, time_step)
histograms_drift = session.presentationwise_spike_counts(
    bin_edges=time_domain,
    stimulus_presentation_ids=drift.index,
    unit_ids=None
)

spont = session.get_presentations_for_stimulus("spontaneous")

# Get the info about the first session of spontaneous acitivty.
first_spont_id = spont.index.values[0]
first_spont_duration = spont.loc[first_spont_id, "stop_time"] - spont.loc[first_spont_id, "start_time"]

# Construct the time domain at 10 ms resolution.
time_step = 1 / 100
time_domain = np.arange(0.0, first_spont_duration + time_step, time_step)

histograms_spont = session.presentationwise_spike_counts(
    bin_edges=time_domain,
    stimulus_presentation_ids=spont.index,
    unit_ids=None
)

# Get the spike histograms for the first presentation of each stimulus only.
spike_counts_spont = histograms_spont[0]
spike_counts_drift = histograms_drift[0]

# Be sure to use the equal amount of time for both histograms - use the duration of the drifting gratings.
max_len=spike_counts_drift.shape[0]

# Get two spike trains in spont activity.
spike_train_1_spont=spike_counts_spont[:max_len, 1]
spike_train_2_spont=spike_counts_spont[:max_len, 2]

# Get two spike trains in drifting gratings activity.
spike_train_1_drift=spike_counts_drift[:max_len, 1]
spike_train_2_drift=spike_counts_drift[:max_len, 2]

# Plot the spike trains for which the correlogram will be computed.

fig, axs = plt.subplots(2, 2,figsize=(14,8))

# Update the figure size.
plt.rcParams.update({"font.size": 15})

axs[0, 0].plot(spike_train_1_spont)
axs[0, 0].set_ylabel("Spike count 2")
axs[0, 0].set_title("Spontaneous activity")
axs[1, 0].plot(spike_train_2_spont)
axs[1 ,0].set_xlabel("Time bins (10 ms)")

axs[0, 1].plot(spike_train_1_drift)
axs[1, 0].set_ylabel("Spike count 1")
axs[0, 1].set_title("Drifting gratings")
axs[1, 1].plot(spike_train_2_drift)
axs[1 ,1].set_xlabel("Time bins (10 ms)")

# Compute the correlogram for spontaneous activity.
xcorr_spont=signal.correlate(spike_train_1_spont,spike_train_2_spont)
xcorr_drift=signal.correlate(spike_train_1_drift,spike_train_2_drift)

# time steps
time_shift_spont=np.arange(-len(xcorr_spont)/2,len(xcorr_spont)/2,1)
time_shift_drift=np.arange(-len(xcorr_drift)/2,len(xcorr_drift)/2,1)

# Plot the cross-correlations for spontaneous and drifting gratings.
plt.figure(figsize=(14,8))
plt.subplot(121)
plt.plot(time_shift_spont,xcorr_spont)
plt.ylabel("Signal correlation")
plt.xlabel("Time steps (10 ms)")
plt.title("Spontaneous activity")
plt.figure
plt.subplot(122)
plt.plot(time_shift_drift,xcorr_drift)
plt.xlabel("Time steps (10 ms)")
plt.title("Drifting gratings")
plt.show()

# Make an array to hold the correlations for all units.
num_units = 100
correlations_spont = np.zeros((num_units, num_units))
correlations_drift = np.zeros((num_units, num_units))

# Compute correlations for the spontaneous activity.
for ii in range(num_units):
    for jj in range(num_units):
        spike_train_1=spike_counts_spont[:max_len, ii]
        spike_train_2=spike_counts_spont[:max_len, jj]
        # only linear correlations
        correlations_spont[ii, jj] = stats.pearsonr(spike_train_1, spike_train_2)[0]
        # correlation for constant values is zero
        if np.isnan(correlations_spont[ii, jj]) == True:
            correlations_spont[ii, jj]=0

# Compute correlations for drifting gratings.
for ii in range(num_units):
    for jj in range(num_units):
        spike_train_1=spike_counts_drift[:max_len, ii]
        spike_train_2=spike_counts_drift[:max_len, jj]
        # only linear correlations
        correlations_drift[ii, jj] = stats.pearsonr(spike_train_1, spike_train_2)[0]
        # correlation for constant values is zero
        if np.isnan(correlations_drift[ii, jj]) == True:
            correlations_drift[ii, jj]=0

# Plot correlation matrix with log10.
# Some units could be silent -> then there are no correlations.
plt.figure(figsize=(14,8))
plt.subplot(121)
plt.imshow(np.log10(correlations_spont+1))
plt.xlabel("Units")
plt.ylabel("Units")
plt.title("Spontaneous activity")
plt.subplot(122)
plt.imshow(np.log10(correlations_drift+1))
plt.title("Drifting gratings")
plt.xlabel("Units")
plt.show()

# Spike waveform features
peak_waveforms = []
for unit_id in unit_list:
    peak_ch = session.units.loc[unit_id, "peak_channel_id"]
    unit_mean_waveforms = session.mean_waveforms[unit_id]
    peak_waveforms.append(unit_mean_waveforms.loc[{"channel_id": peak_ch}])
wv = np.array(peak_waveforms)

# Plot 100 waveforms in this data_set.
fig,ax = plt.subplots(1,1,figsize=(6,4))
for w in wv[:100]:
    ax.plot(w,alpha=0.5)

# Compute trough-to-peak duration.
duration_steps = np.argmax(wv,axis=1) - np.argmin(wv,axis=1)
# Pull the sampling rate from the units table and convert timesteps to ms
sampling_rate = session.units.loc[unit_list, "sampling_rate"]
duration = duration_steps/sampling_rate*1000

# Plot histogram of duration.
plt.hist(duration, bins=30, range=(0,1))
plt.ylabel("N units")
plt.xlabel("Spike duration (ms)")

duration_stored = session.units.loc[unit_list, "waveform_duration"]
plt.scatter(duration, duration_stored)

# Spike-field relationships
# Get spike times and channel info for a single unit.
unit_id = session.units.index.values[0]
spikes = session.spike_times[unit_id]
peak_ch = session.units.loc[unit_id, "peak_channel_id"]
probe_id = session.units.loc[unit_id, "probe_id"]
lfp_full = session.get_lfp(probe_id)
channels = lfp_full.channel.values
channel_closest = channels[np.argmin(np.abs(channels-peak_ch))]
lfp_peak = lfp_full.loc[dict(channel=channel_closest)]

# Time before and after spike
pre_time = 1.
post_time = 1.
array_length = int(np.floor((pre_time+post_time)/(lfp_peak.time.values[1]-lfp_peak.time.values[0])))

# Make list that will contain the LFP around each spike.
spike_triggered_lfp = []

spikes_subset = spikes[1000:-1000:50]
# Loop through every spike.
for i, spike in enumerate(spikes_subset):
    t0 = spike - pre_time
    t1 = spike + post_time
    lfp_subset = lfp_peak.loc[dict(time=slice(t0, t1))].values[:array_length]
    spike_triggered_lfp.append(lfp_subset)
spike_triggered_lfp = np.array(spike_triggered_lfp)
sta_lfp = np.mean(spike_triggered_lfp, axis=0)
plt.plot(sta_lfp)

# Instantaneous phase of oscillatory LFP signals
lfp_subset = lfp_peak.loc[dict(time=slice(10,20))]
v = lfp_subset.values
t = lfp_subset.time.values
fs = 1/(t[1]-t[0])
f, psd = signal.welch(v, fs, nperseg=1000)
f_peak = f[np.argmax(psd)]
print(f"peak frequency: {f_peak} Hz")
freq_window = (f_peak-2, f_peak+2)
filt_order = 3
b, a = signal.butter(filt_order, freq_window, btype="bandpass", fs=fs)
v_filtered = signal.lfilter(b, a, v)
lfp_z = signal.hilbert(v_filtered)
lfp_amp = np.abs(lfp_z)
lfp_phase = np.angle(lfp_z)

# Plot.
plt.figure(figsize=(8,2))
plt.plot(t, v_filtered,"b",label="filtered signal",alpha=.5)
plt.plot(t, lfp_amp,"k",label="amplitude",alpha=.5)
plt.legend(loc="best")
plt.xlabel("Time (s)")
plt.ylabel("Voltage (uV)")
plt.figure(figsize=(8,4))
plt.subplot(3,1,1)
plt.plot(t, v_filtered,"k")
plt.ylabel("Filtered\nVoltage (uV)")
plt.subplot(3,1,2)
plt.plot(t, lfp_amp,"k")
plt.ylabel("Amplitude (uV)")
plt.subplot(3,1,3)
plt.plot(t, lfp_phase,"k")
plt.xlabel("Time (s)")
plt.ylabel("Phase (rad)")

# Tuning curves
stim_table = session.get_presentations_for_stimulus("static_gratings")
stim_ids = stim_table.index.values
session.get_stimulus_parameter_values(stimulus_presentation_ids=stim_ids)
bin_edges = [0, stim_table.duration.min()]
spike_stats = session.presentationwise_spike_counts(bin_edges,stimulus_presentation_ids=stim_ids, unit_ids=unit_list)
spike_stats = spike_stats.to_dataframe().reset_index()
spike_stats = pd.merge(spike_stats, stim_table, on="stimulus_presentation_id", right_index=True)
spike_stats.head()
unit_id = 914686471
data = spike_stats[(spike_stats.unit_id==unit_id) & (spike_stats.spatial_frequency==0.16)]
y = "spike_counts"
x = "orientation"
hue = "phase"
sns.pointplot(data=data, x=x, y=y, hue=hue, dodge=True)
data = spike_stats[(spike_stats.unit_id==unit_id)]
data = data.replace("null", np.nan)
y = "spike_counts"
x = "orientation"
hue = "phase"
col = "spatial_frequency"
sns.catplot(data=data, col=col, x=x, y=y, hue=hue, col_wrap=3, kind="point")
