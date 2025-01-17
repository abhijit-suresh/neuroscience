import matplotlib.pyplot as plt
import nitime.utils as utils
import nitime.timeseries as ts
import nitime.viz as viz
import numpy as np

"""
Calculate signal-to-noise (signal to noise snr) ratio. Where SNR(omega) is the ratio of the signal power and the noise power at the 
frequency band centered on \omega.This equation holde true for a Gaussian channel and is an upper bound for all other cases.
The signal power is estimated as the power of the mean response to repeated presentations of the same signal and the noise power 
is calculated as the average of the power in the deviation from this average in each trial
"""

# Generate auto-regressive sequence as the signal
ar_seq, nz, alpha = utils.ar_generator(N=128, drop_transients=10)
ar_seq -= ar_seq.mean()

# Signal repeated several times with noise
n_trials = 12
fig_snr = []
sample = []
fig_tseries = []

# Add noise to ar_seq to demonstrate effects of adding noise on signal to noise ratio and the 
# calculated information.
for idx, noise in enumerate([1, 10, 50, 100]):
    sample.append(np.ones((n_trials, ar_seq.shape[-1])) + ar_seq)
    n_points = sample[-1].shape[-1]
for trial in  range(n_trials):
    sample[-1][trial] += np.random.randn(sample[-1][trial].shape[0]) * noise
sample_mean = np.mean(sample[-1], 0)

fig_tseries.append(plt.figure())
ax = fig_tseries[-1].add_subplot(1, 1, 1)
ax.plot(sample[-1].T)
ax.plot(ar_seq, "b", linewidth=4)
ax.plot(sample_mean, "r", linewidth=4)
ax.set_xlabel("Time")
ax.set_ylabel("Amplitude")

# low noise
tseries = ts.TimeSeries(sample[-1], sampling_rate=1.)
fig_snr.append(viz.plot_snr(tseries))

# Plot to compare information transmission and the signal to noise ratio between last two noise levels.
ts1 = ts.TimeSeries(sample[-1], sampling_rate=1.)
ts2 = ts.TimeSeries(sample[-2], sampling_rate=1.)
fig_compare = viz.plot_snr_diff(ts1, ts2)
plt.show()
