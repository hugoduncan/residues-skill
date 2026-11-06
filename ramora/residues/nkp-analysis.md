# NKP analysis

Sources: see [../residues.md](../residues.md). Section references (§) refer to O'Reilly 2022. "2020 §" refers to O'Reilly 2020.

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

For the incidence matrix, see [stressors.md](../stressors.md).

## Related

- [../residues.md](../residues.md): index
- [../stressors.md](../stressors.md): stressors, incidence matrix
