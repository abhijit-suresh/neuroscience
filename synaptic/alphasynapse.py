import time
import numpy as np
from numpy import concatenate as cc
import matplotlib.pyplot as plt

"""
Compute the firing of a neuron via alpha function synapse and a (random) input spike train.

The alpha function is often used for desrcribing synaptic conductance with the expression

P_s = (P_max*t / tau_s) * exp((1-t)/tau_s)

in which P_s is the opening probability of a postsynaptic channel. For an isolated snynapse at time t = 0,
we can generate random spike inputs and compute the membrane voltage using an I & F implementation of dV/dt = - V/RC + I/C.
"""
np.random.seed(123)

h = 1. # step size, Euler method, = dt ms
t_max= 200 # ms, simulation time period
tstop = int(t_max/h) # number of time steps
ref = 0 # refractory period counter

thr = 0.9 # threshold for random spikes
spike_train = np.random.rand(tstop) > thr

def alpha_():
    """
    Alpha function for synaptic conductance
    """
