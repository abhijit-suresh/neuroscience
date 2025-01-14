import numpy as np

"""
We model Lobula plate tangential cells (LPTC lptc) used in the fly visual ganglia. The lobula plate is
in the posterior part of the lobula complex (the third visual ganglion of the fly eye). We use electrophysiological
recordings to study the large diameter of the intracellular processes. The integrating neurons can be modeled on a 
biophysical level with direct recordings of their membrane properties. 

We measure the response feature of LPTCs with the spatial integration characteristics when enlarging the area
in which the motion stimulus is displayed. The response saturates signficantly not only for motion along the preferred
direction, but also along the nulll direction. The gain control gives us different saturation plateaus.
"""

def V(E, g, gl):
    """
    Given a list of excitatory and inhibitory potentials E (tuple array) and excitatory and inhibitory conductances g 
    (tuple array) and a leak conductance gl, calcualte the membrane potential V.
    """
    num = 0
    den = 0
    for i in range(len(E)):
        num += E[i][0]*g[i][0] + E[i][1]*g[i][1]
        den += g[i][0] + g[i][1] + gl
    return num / den

"""
As the membrane potential saturates, we can calulate the activation ratio of the opposing inputs (exchitation and inhibition).

c ~= cos(R - phi(omega)) / cos(R + phi(omega))
"""
