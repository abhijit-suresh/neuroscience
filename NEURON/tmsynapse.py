import neuron
import numpy
import matplotlib.pyplot as plt

from neuron import h

# Load external files & initialize.
neuron.h.load_file("stdrun.hoc")
neuron.h.stdinit()

"""
Tsodyks-Markram (tsodyks markram) model.
"""

soma = neuron.h.Section()
soma.L = 40
soma.diam = 40
soma.insert("pas")

# Configure the passive biophysics.
for sec in h.allsec():
    sec.Ra = 100
    sec.cm = 1

synapse = h.TsodyksMarkram_AMPA_NMDA(soma(0.5))

stimulator = h.VecStim()
spike_times = [100.0, 150.0, 200.0, 250.0, 300.0, 350.0, 400.0, 450.0, 950.0]
spikes_vector = h.Vector(spike_times)
stimulator.play(spikes_vector)

connection = h.NetCon(stimulator, synapse)
connection.weight[0] = 1.0  # In units of [nS] due to the gmax scaling factor in our .mod file.

g_syn = h.Vector()
g_syn.record(synapse._ref_g)
i_syn = h.Vector()
i_syn.record(synapse._ref_i)
v_soma = h.Vector()
v_soma.record(soma(0.5)._ref_v)
time = h.Vector()
time.record(neuron.h._ref_t)
R_syn = h.Vector()
R_syn.record(synapse._ref_R)
Use_syn = h.Vector()
Use_syn.record(synapse._ref_Use)

synapse.gmax_AMPA = 0.001 # uS
synapse.gmax_NMDA = 0.7 * 0.001 # uS - 0.7 is a biologically typical ratio of NMDA to AMPA conductance
synapse.mg = 1.0 # mM

synapse.U1 = 0.2 # Baseline release probability
synapse.tau_rec = 200 # ms - recovery from depression
synapse.tau_facil = 200 # ms - relaxation from facilitation

h.tstop = 1000.0 # ms
neuron.h.run()
