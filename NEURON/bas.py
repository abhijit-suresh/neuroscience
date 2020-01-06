from neuron import h
from neuron.units import ms, mV

"""
Ball-and-stick (ball and stick) model
"""

h.load_file("stdrun.hoc")

class BallAndStick:
    def __init__(self, gid):
        self._gid = gid
        self._setup_morphology()
        self._setup_biophysics()
    def _setup_morphology(self):
        self.soma = h.Section(name="soma", cell=self)
        self.dend = h.Section(name="dend", cell=self)
        self.dend.connect(self.soma)
        self.all = self.soma.wholetree()
        self.soma.L = self.soma.diam = 12.6157
        self.dend.L = 200
        self.dend.diam = 1
    def _setup_biophysics(self):
        for sec in self.all:
            sec.Ra = 100 # Axial resistance in Ohm * cm
            sec.cm = 1 # Membrane capacitance in micro Farads / cm^2
        self.soma.insert("hh")                                          
        for seg in self.soma:
            seg.hh.gnabar = 0.12 # Sodium conductance in S/cm2
            seg.hh.gkbar = 0.036 # Potassium conductance in S/cm2
            seg.hh.gl = 0.0003 # Leak conductance in S/cm2
            seg.hh.el = -54.3 # Reversal potential in mV
        # Insert passive current in the dendrite.                       
        self.dend.insert("pas")                                        
        for seg in self.dend:                                          
            seg.pas.g = 0.001 # Passive conductance in S/cm2          
            seg.pas.e = -65 # Leak reversal potential mV            
    def __repr__(self):
        return "BallAndStick[{}]".format(self._gid)

my_cell = BallAndStick(0)

# stimulation
stim = h.IClamp(my_cell.dend(1))
stim.get_segment()

# Check attributes.
print(", ".join(item for item in dir(stim) if not item.startswith("__")))

stim.delay = 5
stim.dur = 1
stim.amp = 0.1

# recording
soma_v = h.Vector().record(my_cell.soma(0.5)._ref_v)
t = h.Vector().record(h._ref_t)

# Run the simulation.
h.finitialize(-65 * mV)
