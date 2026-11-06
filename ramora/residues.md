# Residues

Source: O'Reilly, B. M. (2022). Residuality Theory, random simulation, and attractor networks. Procedia Computer Science 201: 639–645. https://doi.org/10.1016/j.procs.2022.03.084

Overview used: https://github.com/pragsmike/cyberneutics/blob/main/references/papers/Residuality-Oreilly-2022.md

Section references (§) refer to the source.

## Terms

| Term | Part of speech | Use |
|---|---|---|
| residue | noun | the subset of nodes. See Definition. |
| residual | adjective | residual analysis, residual index, residual architecture |
| residuality | noun | the name of the theory |

## Definition

A stressor affects the system. The architect isolates the affected nodes and the relevant nodes. This subset of nodes is the residue. (§1.5)

The residue is what remains of the system after a stressor. The future of the system is a function of its residue. (§1.6, statement 3)

For stressors, see [stressors.md](stressors.md).

## Attractors

An attractor is a state that the system visits most often. The number of attractors is limited. (§1.5, §3.2)

A stressor can move the system from one attractor to a different attractor.

## Augmenting a residue

To augment a residue is to change its structure. The change makes the transition to a possible new state easier. (§1.5)

## Residue as an abstraction

A residue is a container. With residues, the architect examines the full system through many stressors and attractor transitions. These occur at different times and in different orders. The architect does this before committing to an architecture. Thus thought about possible futures becomes easier. (§1.5)

Residual analysis models residues, not components directly. Thus it can identify hyperliminal coupling at design time. (§2)

## Network levels

- Software is a network of residues.
- A residue is a network of components.
- A component is a network of functions.
- Information flows connect functions to nodes in the hyperliminal network. (§3.3)

## NKP analysis

NKP analysis is step 2 of the two-step algorithm of residual analysis. It applies the variables of Kauffman networks to the software part of the network. (§3.2, §3.3)

| Variable | Kauffman network | Software |
|---|---|---|
| N | number of nodes | components |
| K | highest number of connections of one node | connections or calls between components |
| P | bias of a node toward a particular result | contracts, schemas, policies and fewer code branches increase P |

Effects (§3.2, §3.3):

- Higher N and higher K give many more attractors.
- Higher P gives fewer outcomes. The network is easier to manage.
- The correct balance of N, K and P moves the network to the edge of chaos. At the edge of chaos the network is stable. It can also move between attractors.
- Too much order (few attractors): the network is vulnerable to unexpected changes.
- Too much disorder (many attractors): external stress affects the network easily.

NKP analysis gives clear terms for loose coupling, cohesion and component granularity. (§3.3)

## Adjacency matrix

An adjacency matrix is a directed matrix. It shows dependency between nodes of the same type: processes, information flows, software functions or software components. (§3.3.1)

- Symmetry shows multidirectional coupling. Stressors can spread through this coupling.
- Use the matrix to find unnecessary links and interdependent nodes.
- Remove unnecessary links. Combine interdependent nodes. This decreases N and K and increases P.
- The matrix is similar to a Design Structure Matrix.

For the incidence matrix, see [stressors.md](stressors.md).

## Residual index Ri

Ri measures the result of residual analysis (§4):

1. Divide the stressors into a training set and a testing set.
2. Do the random simulation and the network analysis with the training set. The result is the residual architecture.
3. Apply the testing set to the residual architecture and to the naive architecture. The naive architecture is the control.
4. Calculate Ri.

Ri > 0 shows a successful intervention. The residual architecture is more likely to survive unknown stress than the naive architecture.

Example: a student lab gave Ri values of 0.27 to 0.57 after a few hours of work. This was not a controlled experiment. It is not proof. (§4)

The source does not give the formula for Ri. The formula is in O'Reilly (2020), "An introduction to residuality theory", Procedia Computer Science 170: 875–880. Verify the formula against that paper before use.

## Three statements of residuality theory (§1.6)

1. Enterprise software systems are ordered systems in disordered environments. They are hyperliminal systems.
2. These systems will experience stress that they are not designed for. The disordered environment is not predictable.
3. The future of the system is a function of its residue: what remains after stress.

## Related

- [stressors.md](stressors.md): stressor, hyperliminal coupling, random simulation, incidence matrix
