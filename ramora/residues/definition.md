# Residue: definition

Sources: see [../residues.md](../residues.md). Section references (§) refer to O'Reilly 2022. "2020 §" refers to O'Reilly 2020.

## Terms

| Term | Part of speech | Use |
|---|---|---|
| residue | noun | the subset of nodes. See Definition. |
| residual | adjective | residual analysis, residual index, residual architecture |
| residuality | noun | the property of having residues when exposed to stress (2020 §2). Also the name of the theory. |

## Definition

A stressor affects the system. The architect isolates the affected nodes and the relevant nodes. This subset of nodes is the residue. (§1.5)

The residue is what remains of the system after a stressor. The future of the system is a function of its residue. (§1.6, statement 3)

A residue is a set of components, infrastructures, people and information flows. A flow is a transfer of data from one actor to a different actor. (2020 §2)

Residues are not visible until a stress makes them visible. Stressor analysis makes them visible at design time. (2020 §2, §4.1)

For stressors, see [stressors.md](../stressors.md).

## Attractors

An attractor is a state that the system visits most often. The number of attractors is limited. (§1.5, §3.2)

A stressor can move the system from one attractor to a different attractor.

## Augmenting a residue

To augment a residue is to change its structure. The change makes the transition to a possible new state easier. (§1.5)

## Residue as an abstraction

A residue is a container. With residues, the architect examines the full system through many stressors and attractor transitions. These occur at different times and in different orders. The architect does this before committing to an architecture. Thus thought about possible futures becomes easier. (§1.5)

Residual analysis models residues, not components directly. Thus it can identify hyperliminal coupling at design time. (§2)

An architecture is multidimensional. Each residue is one dimension. The most important boundaries are between residues, not between components or use cases. (2020 §4.1)

## Network levels

- Software is a network of residues.
- A residue is a network of components.
- A component is a network of functions.
- Information flows connect functions to nodes in the hyperliminal network. (§3.3)

## Residues and stressors

The set of possible residues is smaller than the set of possible stressors (Ashby's Law of Requisite Variety). Thus one residue relates to many stressors. (2020 §3)

A residue that is changed for one stressor can also survive other stressors. These stressors affect the same flows. The system can use the new structures in novel ways (exaptation). This depends on residual coverage: the number of the actual residues that the analysis identifies. (2020 §3)

Residues with similar incidence matrices can share components. Where residues are different, put the different components into separate services. (2020 §3)

## Three statements of residuality theory (§1.6)

1. Enterprise software systems are ordered systems in disordered environments. They are hyperliminal systems.
2. These systems will experience stress that they are not designed for. The disordered environment is not predictable.
3. The future of the system is a function of its residue: what remains after stress.

## Related

- [../residues.md](../residues.md): index
- [../stressors.md](../stressors.md): stressors, incidence matrix
