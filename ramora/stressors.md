# Stressors

Source: O'Reilly, B. M. (2022). Residuality Theory, random simulation, and attractor networks. Procedia Computer Science 201: 639–645. https://doi.org/10.1016/j.procs.2022.03.084

Overview used: https://github.com/pragsmike/cyberneutics/blob/main/references/papers/Residuality-Oreilly-2022.md

Second source: O'Reilly, B. M. (2020). An introduction to residuality theory: Software design heuristics for complex systems. Procedia Computer Science 170: 875–880. https://doi.org/10.1016/j.procs.2020.03.120

Section references (§) refer to the 2022 source.

## Definition

A stressor is an event in the unknown future of a system. The system is not designed for this event. (§1.2)

## Origin of stressors

An enterprise software system is an ordered system. An ordered system is predictable, mappable and testable.

The software operates in a disordered environment: the enterprise. A disordered environment is dynamic. It grows. It is not predictable.

An ordered system inside a disordered system is a hyperliminal system. (§1.3)

Stressors come from the disordered environment. That environment is not predictable. Thus the system will always experience stressors. (§1.6, statement 2)

## Properties

- A stressor is not a requirement.
- A stressor is not a risk. No probability filter and no impact filter apply.
- Probability is not relevant. A stressor with near-zero probability is valid.
- Nonsense stressors and impossible events are valid. (§3.1)
- The set of possible stressors is very large. It is not possible to list all stressors. No probability distribution exists for them. (§3.1)

## Hyperliminal coupling

If two nodes in a network each have a relationship with a third node, the two nodes probably have a relationship.

Thus, if one stressor affects two software components, those components are coupled. This is hyperliminal coupling. (§1.4)

The designer cannot see this coupling until the stressor occurs. Stressor analysis makes the coupling visible at design time. (§2)

## Why random stressors work

Traditional methods decrease the number of futures that they examine (§3.1):

- Requirements engineering makes precise statements about what to build.
- Risk management filters possible events by probability and impact.

These methods are already random simulations. They are guesses from experience and bias. Their results return to areas of high probability (curse of dimensionality). (§3.1)

Residual analysis increases the randomness and the sample size of the simulation. It uses random stressors. The simulation collects narratives. It does not use a mathematical model of the environment. (§3.1)

The business environment has many more attractors than the software. Thus many different stressors move the software to the same attractor. A stressor with almost zero probability can point to an attractor. The system can need that attractor to survive a different, less visible stressor. (§4)

Thus random stressors show the unknown K: hidden connections, that is, hyperliminal coupling. (§4) For K and attractors, see [residues/nkp-analysis.md](residues/nkp-analysis.md) and [residues/definition.md](residues/definition.md).

## Stressor analysis

Stressor analysis is step 1 of the two-step algorithm of residual analysis (§2, §4):

1. Random simulation of the environment with stressors.
2. Network analysis of the software structure (NKP analysis). See [residues/nkp-analysis.md](residues/nkp-analysis.md).

The two steps are present implicitly in all software design methods. Residual analysis makes them explicit and increases their effect. (§4, §5)

## Incidence matrix

An incidence matrix maps stressors against one of: residues, processes, information flows, software functions, software components. (§3.3.2)

The matrix shows:

- the most vulnerable components
- the most dangerous stressors
- components with similar patterns. These components have hyperliminal coupling. Group them.

Use the incidence matrix together with the adjacency matrix. See [residues/nkp-analysis.md](residues/nkp-analysis.md).

## Training set and testing set

Divide the stressors into a training set and a testing set. (§4)

- Use the training set to drive the design.
- Use the testing set after the design to measure the result with the residual index Ri. See [residues/residual-index.md](residues/residual-index.md).
- Repeat with different training sets and testing sets, in different orders (bagging and boosting). (O'Reilly 2020 §3)

One residue relates to many stressors. Thus a change for one stressor can also help the system survive other stressors. See [residues/definition.md](residues/definition.md).

## Related

- [residues.md](residues.md): index of residue documents: definition, attractors, NKP analysis, adjacency matrix, residual index
