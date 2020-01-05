import neuron
import numpy
import matplotlib.pyplot as plt

from neuron import h

"""
AMPA-NMDA synapse model
"""

# Load external files & initialize
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
