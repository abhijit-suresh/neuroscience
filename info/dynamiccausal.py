import scipy.sparse as sps

"""
Dynamic causal modelling (DCM) concerns the relation existing between cognitive functions and their 
neurobiological “signature” (the spatio-temporal properties of brain activity) requires an understanding 
of how information is transmitted through brain networks. The ambition here is to ask questions such as: 
"what is the nature of the information that region A passes on to region B"? This stems from the notion 
of functional integration, which views function as an emergent property of brain networks. Dynamic causal 
modelling or DCM was developed specifically to address this question.
"""

def erp(x, u, P, M):
    """
    Event-related potential for state vector x with the following:
    x[1] - voltage (spiny stellate cells)
    x[2] - voltage (pyramidal cells) +ve
    x[3] - voltage (pyramidal cells) -ve
    x[4] - current (spiny stellate cells)    depolarizing
    x[5] - current (pyramidal cells)         depolarizing
    x[6] - current (pyramidal cells)         hyperpolarizing
    x[7] - voltage (inhibitory interneurons)
    x[8] - current (inhibitory interneurons) depolarizing
    x[9] - voltage (pyramidal cells) 
    Return f (dx(t)/dt = f(x(t))), J (df(t)/dx(t)), and D (delay operator dx(t)/dt)
    """
    n = len(P["A"][0]) # number of sources

