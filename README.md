# MOOSE-Notebooks

These notebooks present hands-on tutorials for topics in modeling in Neuroscience and Systems Biology. The contents are divided into three groups, Beginner, Intermediate, and Advanced.

## How to run these notebooks
These notebooks use the MOOSE neuro-simulator. It is available as a Python module. You can either install it on your own computer, or install it on a [Google Colab](https://colab.research.google.com/) environment. 

## Beginner
1. [Using MOOSE on Colab](MOOSE_on_Colab.ipynb)
2. [MOOSE overview](Moose_overview.ipynb)

## Biophysics of Neurons
4. [Resting membrane potential](Resting_membrane_potential.ipynb)
   Discussion of Nernst-Planck and Nernst equation and Goldman-Hodgkin-Katz equation
5. [Getting started with compartmental modelling in MOOSE](Getting_started_with_compartmental_modelling_in_MOOSE.ipynb)
   Shows how to create a passive neuronal compartment in MOOSE
6. [More complex current injection protocol](More_complex_current_injection_protocol.ipynb)
   Shows how to generate various patterns of (current) pulses for injecting into a compartment
7. [Multi-compartmental neuron model](Multi-compartmental_neuron_model.ipynb)
   Describes how you can connect several compartments to create a neuronal cable
8. [Cable theory](Cable_theory.ipynb)
   Derives the cable equation and then shows its approximation using a voltage clamped multicompartmental cable
9. [Hodgkin and Huxley's model of K+ current](Action_potentials_K_channel.ipynb)
   Implements Hodgkin and Huxley's model of K+ current. This is the first step towards modeling action potentials in the squid giant axon.
10. [Hodgkin and Huxley's model of Na+ current](Action_potentials_Na_channel.ipynb)
   Implements Hodgkin and Huxley's model of Na+ current. The Na+ current is responsible for depolarizing the neuron for an action potential, whereas the K+ current repolarizes it.
11. [Action potentials](Action_potentials.ipynb)
   Puts together the Na+ and K+ currents to demonstrate Hodgkin and Huxley's model of action potential generation in the squid giant axon.

## Biochemistry of Neurons

1. [Modeling a simple chemical reaction](Chemical_kinetics_introduction.ipynb)

## Intermediate
12. [Synapses](Synapses.ipynb)
   Explains the components of the basic synapse model in MOOSE. There can be multiple ways to model a synapse at different complexities, all based on these basic ideas.
13. [Leaky integrate and fire (LIF) neurons and synapse](Leaky_integrate_and_fire_neuron.ipynb)
   Implementation of a network of simple integrate-and-fire neurons connected via synapses.
14. [Synapse between two biophysical model neurons](HH_comps_with_synapse.ipynb)
    Two single-compartment neuron models with Hodgkin-Huxley dynamics connected by a synapse.
