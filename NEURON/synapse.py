import neuron
import numpy
import matplotlib.pyplot as plt

from neuron import h

"""
Excitatory and inhibitory synapsae
"""

# Load external files & initialize.
neuron.h.load_file("stdrun.hoc")
neuron.h.stdinit()

soma = neuron.h.Section()
soma.L = 40
soma.diam = 40
soma.insert("pas")

# Configure the passive biophysics.
for sec in h.allsec():
    sec.Ra = 100
    sec.cm = 1

synapse = h.Exp2Syn(soma(0.5))
synapse.tau1 = 0.5 # [ms]
synapse.tau2 = 10.0 # [ms]
synapse.e = -80.0 
