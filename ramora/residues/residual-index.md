# Residual index Ri

Sources: see [../residues.md](../residues.md). Section references (§) refer to O'Reilly 2022. "2020 §" refers to O'Reilly 2020.

Ri measures the result of residual analysis (§4; 2020 §3):

1. Divide the stressors into a training set and a testing set.
2. Do the random simulation and the network analysis with the training set. The result is the residual architecture.
3. Apply the testing set to the residual architecture and to the naive architecture. The naive architecture is the control.
4. Calculate Ri.

Formula (§4, equation image on p. 644):

- S: total number of stressors
- N: number of stressors that the naive architecture survives
- R: number of stressors that the residual architecture survives
- If neither architecture survives a stressor, add 1 to N or to R. Add it for the architecture that survives the stressor better.

```
Ri = (R - N) / S        -1 < Ri < 1
```

Ri > 0 shows a successful intervention. The residual architecture is more likely to survive unknown stress than the naive architecture.

Example: a student lab gave Ri values of 0.27 to 0.57 after a few hours of work. This was not a controlled experiment. It is not proof. (§4)

Iterate with different training sets and testing sets, in different orders (bagging and boosting). Compare the candidate architectures. (2020 §3)

## Related

- [../residues.md](../residues.md): index
- [../stressors.md](../stressors.md): stressors, incidence matrix
