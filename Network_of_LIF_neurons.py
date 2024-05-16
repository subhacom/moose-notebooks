# Imports
import numpy as np
import matplotlib.pyplot as plt
import moose

##
rng = np.random.default_rng()  # this is our random number generator

N = 1000
N_E = int(0.8 * N)  # number of excitatory neurons
N_I = N - N_E  # number of inhibitory neurons

EPSILON = 0.1  # fraction of inputs from each type

theta = 20e-3  # spiking threshold for all neurons
Vr = 10e-3  # reset voltage 10 mV
t_rp = 2e-3  # refractory period 2 ms
tau_E = 20e-3  #
##########
# while J > 0 is PSP amplitude for all excitatory synapses,
# PSP amplitude for inhibitory synapses is -gJ. We name g is `ginh`
J = 1.0  # efficacy of excitatory synapse
ginh = 1.0  # scale factor for inhibitory synapses
# "External synapses are activated by independent Poisson processes with rate v_ext"
nu_ext = 100.0

C_E = int(EPSILON * N_E)  # number of excitatory connections per neuron
C_I = int(EPSILON * N_I)  # number of inhibitory connections per neuron

C_EXT = C_E  # number of external excitatory connections per neuron

DELAY = 1e-3  # synaptic delay

##########
# containers
if moose.exists('/sim'):
    moose.delete('/sim')

sim = moose.Neutral('/sim')
model = moose.Neutral(f'{sim.path}/model')
data = moose.Neutral(f'{sim.path}/data')
##########
netA = moose.LIF(f'{model.path}/networkA', N)

netA.vec.thresh = theta

# LIF class uses the logic of RC-Compartment to compute time course.
# Thus it uses Rm and Cm instead of tau. Time constant tau = Rm * Cm.
netA.vec.Rm = 1.0
netA.vec.Cm = tau_E  # tau = Rm * Cm, so Cm = tau_E / Rm
netA.vec.refractoryPeriod = t_rp
netA.vec.vReset = Vr
netA.vec.Em = 0  # resting voltage
netA.vec.initVm = 0  # initial voltage

## Make synapses
synA = moose.SimpleSynHandler(f'{netA.path}/syn', N)
# Make one-to-one connections from SynHandler elements to LIF elements
moose.connect(synA, 'activationOut', netA, 'activation', 'OneToOne')

# Set up the synaptic connections - this is the crux of the model
for ii in range(N):
    synA.vec[ii].numSynapses = int(C_E + C_I + C_EXT)
    # We designate first N_E neurons to be excitatory and the rest (N_I = N - N_E) inhibitory
    # and select C_E neurons out of those as presynaptic to the current neuron (#ii)
    pre_list = rng.choice(np.arange(N_E), C_E)
    for jj, pre in enumerate(pre_list):
        syn = synA.vec[ii].synapse[jj]
        moose.connect(netA.vec[pre], 'spikeOut', syn, 'addSpike')
        syn.weight = J
    # Select C_I inhibitory presynaptic neurons from the remaining neurons (N_E+1, N_E+2, ..., N)
    pre_list = rng.choice(np.arange(N_E, N), C_I)
    for jj, pre in enumerate(pre_list):
        syn = synA.vec[ii].synapse[jj]
        moose.connect(netA.vec[pre], 'spikeOut', syn, 'addSpike')
        syn.weight = -ginh * J

# External inputs: independent C_EXT elements for each of N neurons
extern = moose.RandSpike(f'{model.path}/external', N * C_EXT)
for vv in extern.vec:
    vv.doPeriodic = False
    vv.rate = nu_ext
for ii in range(N):
    for jj in range(C_EXT):
        moose.connect(
            extern.vec[ii * C_EXT + jj],
            'spikeOut',
            synA.vec[ii].synapse[C_I + C_E + jj],
            'addSpike',
        )

## Data recording
# spike trains from individual neurons
spiketabs_exc = []
spiketabs_inh = []
vtabs_exc = []
vtabs_inh = []
for ii in range(N):
    tab = moose.Table(f'{data.path}/spikes_{ii}')
    moose.connect(netA.vec[ii], 'spikeOut', tab, 'input')
    if ii < N_E:
        spiketabs_exc.append(tab)
    else:
        spiketabs_inh.append(tab)

NUM_VM = 10
idx_exc = rng.choice(N_E, size=NUM_VM)
idx_inh = rng.choice(np.arange(N_E, N), size=NUM_VM)
for ii in idx_exc:
    tab = moose.Table(f'{data.path}/vm_{ii}')
    moose.connect(tab, 'requestOut', netA.vec[ii], 'getVm')
    vtabs_exc.append(tab)
for ii in idx_inh:
    tab = moose.Table(f'{data.path}/vm_{ii}')
    moose.connect(tab, 'requestOut', netA.vec[ii], 'getVm')
    vtabs_inh.append(tab)


runtime = 1000e-3    
moose.reinit()
moose.start(runtime)

fig, axes = plt.subplots()
for ii, tab in enumerate(vtabs_exc + vtabs_inh):    
    axes.plot(tab.dt * np.arange(len(tab.vector)), ii + tab.vector)
    print(max(tab.vector), min(tab.vector))
    
plt.show()    
