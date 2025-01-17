import itertools
import numpy as np
import scipy as sp

"""
When we observe spike train of a sensory neuron, we learn about many different aspects of the stimulus.
This way, we gain information. Shannon entropy is closely related to information. We can think about information transmission by sensory neurons in terms of
various parts of the spike train as part of stimulus space.

In classical mechanics, particles can take on a continuous range of positions and velocities. There"s no natural scale for the precisino of the measurements.
"""

def totalProb(variableProbs):
    """
    The additivity of information mean that for any distribution of N independent variables,
    the probability of each of them occuring is the product of each of the individual variables.
    """
    return itertools.product(variableProbs)

def entropySum(variableProbs, k):
    """
    Summation notion of entropy as logarithm of the number of possible states the systme can occupy.
    k is a constant.
    """
    S = 0
    for prob in variableProbs:
        S += (prob * np.log(prob))
    S *= -k
    return S

def entropyIntIntegrand(p):
    """
    The inside of the integral for the integral notion of entropy.
    """
    return p * np.log(p))

def entropyInt(variableProbs, k):
    """
    Integral notion of entropy.
    """
    S = sp.integrate(entropyIntIntegrand(prob for prob in variableProbs), 0, 1)
    return S *= -k

def entropyDiscrete(deltaV, sigma):
    """
    If we measure voltage V in milliVolts then we can take the continuous voltage variable and place it in discrete bins of size
    ΔV. This equation works if ΔV is very small. sigma is the variance.
    """
    return (1/2)*np.log2(2*np.pi*exp((sigma**2/(deltaV**2)))

def entropyConditionalIntegrand(P):
    """
    Entropy conditional integrand
    """
    return P*np.log2(P))
    
def entropyConditional(conditionalProbs):
    """
    Conditional entropy uses a conditional distribution of probabilities that measure rrelative
    likelihood of different input signals x given that we have observed a particular output value y.
    """
    return -sp.integrate(entropyConditionalIntegrand(prob for prob in conditionalProbs), 0, 1)
    
def probReadout(y):
    """
    Readout y is porportional to s with some gain g. This is the mutual information of the Gaussian channel. si s a signal and we have an s-detector
    that gives us a readout y with some gain g. y is a list of values of which we calculate the variance for this function.
    """
    return (1/np.sqrt(2 * np.pi * np.var(y)**2)) * exp(-y**2)/(2*np.var(y**2))

"""
To use these signals in a biological context we need to generalize a bit and consider signals that vary in time.
We use time-dependent signals. We want to describe a function of time f(t) and confine our attention to a time interval of size T with
0 < t < T. We can use a Fourier series, sum of sine and cosine functions. They later become helpful in constructing power spectral density.
"""

period = 2*np.pi

def cn(n):
    """
    Complex Fourier coefficients for corresponding real number n.
    """
    c = y*np.exp(-1j*2*n*np.pi*time/period)
    return c.sum()/c.size

def fourier(x, Nh):
    """
    Calculate the Fourier series and sum it over data Nh with interval x.
    """
    f = np.array([2*cn(i)*np.exp(1j*2*i*np.pi*x/period) for i in range(1,Nh+1)])
    return f.sum()

"""
To compute the information transmission for signals in the presence of noise,
we note that since different Fourier coefficients are independent, the information carried by each
coefficient can just be added up to give the total information. Once more we look at signals and noise in a fixed time
window 0 < t < T.
"""

omega = 3

def omega(snr, r):
    """
    Gaussian variance of noise.
    """
    return snr*r

def informationTransmission(snr):
    """
    As described above. snr is the signal to noise ratio for the discrete frequencies (omega).
    """
    I = 0
    for n in range(-np.inf, np.inf):
        I += (1/2) * np.log2(1 + omega(snr, n))
    return I

"""
If each photon counted by a receptor cell triggers a sterotyped voltage pulse, or "quantum bump", then if the photons
arrive from an ordinary light source we will have the a spectrum of constant noise equal to 1/R in which R is the photon counting rate.

Given the effective contrast noise psectra of the receptor cells and of the large monoopolar cells, we can compute how much information these cells
provide us about the visual world.
"""

def N_eff(N_v, T):
    """
    N_v is the spectrum of the voltage noise. T is the response of the cell to a contrast pulse at time 0.
    """
    return N_v / abs(T)**2

"""
Maximizing the rate of information transmission is done with noisewhitening. To transmit the maximum amount of information possible given a fixed total signal variance, the power spectrum
of the signals should be matched to the power spectrum of the noise in the system.

Both the photoreceptor and the large monopolar cell produce graded responses but there is an element of discreteness to synaptic transmission itself.
Chemical synapses release transmitters packaged in vesicles.
"""

def probDist(n, a):
    return n * a

def infoSpikeCount(prob, n, a):
    """
    Given probability prob of a certain amplitude, a probability distribution probDist, and amplitude A of the stimulus,
    the information the spike counts provides about the stimulus amplitude can be calculated.
    """
    prob_n = (1/K) * probDist(n, a) # Overall probability of observing n spkes
    return prob * np.log2(prob/prob_n)

"""
In more complicated experiments, we can measure the synergy among individual spike trains.
"""

def diracdelta(a=1, x):
    """
    Dirac delta function is a generalized function to model the density of an idealized point mass
    or point charge as a function equal to zero every except for at x = 0. It has an integral over
    the entire real line equal to one.  
    """
    if x != 0:
        return 0
    else:
        return (1/np.pi)*np.exp(x)**2

def synergy(a, b, t):
    """
    For a certain time point t, calcualte the synergy between two synaptic signals in which
    a and b are given arrays of time points for spike a and spike b.
    """
    trainA = 0 # spike train A
    trainB = 0 # spike train B
    for i in a: # for spike trains a and b, sum up the unit impulses (given as Dirac delta functions) over time
        trainA += diracdelta(t-i) # if we average train A and train B over multiple trials
    for i in b:                   # we can get a time-dependent spike rate.
        trainB += diracdelta(t-i)

def psth(binwidth=3, spikes=np.array([0.8, 1.3, 6, 6.2, 7, 10, 11.2, 15.7, 16]), triggers=np.array([0, 5, 15]), counts=[0]*binwidth, t-1):
    """
    We can use the perstimulus time histogram (psth) to investigate the dynamics
    of correlation and to provide a bit more sensitive means of detecting correlation than
    a one-dimensional crosscorrelogram could.
    """
    # create a perstimulus histogram for example purposes
    for i in range(triggers.size - 1):
        tmpCounts, tmpEdges = np.histogram(spikes, bins = bin_width, range = (triggers[i], triggers[i+1]))
        counts += t

"""
Combining two perstimulus time histgrams we can create a joint perstimulus time histogram (jpsth).

The Information integration theory of consciousness (IIT) draws on the notion of integrated information, 
symbolized by Φ, as a way to explain generic consciousness. 
IIT defines integrated information in terms of the effective information carried by the parts of the system in 
light of its causal profile. For example, we can focus on a part of the whole circuit, say two 
connected nodes, and compute the effective information that can be carried by this microcircuit. 
The system carries integrated information if the effective informational content of the whole is 
greater than the sum of the informational content of the parts. If there is no partitioning where 
the summed informational content of the parts equals the whole, then the system as a whole carries 
integrated information and it has a positive value for Φ. Intuitively, the interaction of the parts 
adds more to the system than the parts do alone.

In recent perceptual neuroscience, an alternative picture of neural representational content often 
tied to Bayesian approaches to perceptual computation has gained traction (for accessible discussions, 
see Colombo & Seriès "Bayes in the Brain—On Bayesian Modelling in Neuroscience" and Rescorla "Bayesian 
Perceptual Psychology"). On Bayesian models, extracting information from populations of MT (middle temporal) 
neurons does not yield a specific value of motion direction but rather a probability density function, 
across the space of possible motion directions (for a philosophical discussion of neural probabilistic 
codes, see Shea "Neural Signalling of Probabilistic Vectors"). A key idea is not the generation of specific values 
as what neurons represent, say 0 degree motion as proposed earlier, but rather the conceptualization 
of the population response as reflecting uncertainty inherent in neural activity given noise.
"""
