import numpy as np

"""
Since pyramidal cell are aligned in parallel, they form a dipole layer of thickness d
when they are synchronized within a cortical molecule. We identify these molecules with
teh anatomical columns in order to collective dipole field potential (as local field potential
generated by a mass of apprxoiamtely 10k pyramidal cells).

The differential of current is proportional to the infinitesimal area in cylindrical coordinates.
"""

dI = j * dA

"""
Where the current density j is assumed ot be constsnat scalar within one column.
The differneital of the potential dphi at a distacne z perpendcicular to a cortical column
"""
