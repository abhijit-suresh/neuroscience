import numpy as np
import scipy.signal as signal
import nitime.algorithms as nt_alg
import nitime.utils as nt_ut
import matplotlib.pyplot as pp

"""
Another application of the Slepian functions is to estimate the complex demodulate of a 
narrowband signal. This signal is normally of interest in neuroimaging when finding the 
lowpass power envelope and the instantaneous phase. The traditional technique uses the 
Hilbert transform to find the analytic signal. However, this approach suffers problems of 
bias and reliability, much like the periodogram suffers in PSD estimation. Once again, a 
multi-taper approach can provide an estimate with lower variance.


"""
