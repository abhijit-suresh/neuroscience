import matplotlib.pyplot as plt
import numpy as np

"""
Leaky integrate and fire (leaky-integrate-and-fire LIF) 
"""

# Initialize vairables.
T = 50 # total time to simulate (msec)
dt = 0.125 # simulation time step (msec)
time = arange(0, T+dt, dt) # time array
trest = 0 # initial refractory time
