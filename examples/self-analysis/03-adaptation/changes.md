# Step 3: adapt-design — Changes

Index: [../03-adaptation.md](../03-adaptation.md)

## Changes

| ID | Change | Skill | Stressors |
|---|---|---|---|
| C01 | Scope: if the design is too large to read, agree a scope or a coarse level with the user. Record the level of detail. | gs, fhc | S05, S34 |
| C02 | One criteria record: essential functions and acceptable effort. The user confirms it before the first survival decision. ad and ed use it unchanged. A change to it makes ad recheck. | ad, ed | S11, S40 |
| C03 | Input check: if the naive or the adapted design is missing, stop and ask. Never derive the naive design from the adapted one. | ed | S12 |
| C04 | Run record: one directory for each analysis, with fixed files (design, stressors with set column, coupling, criteria, changes, naive, adapted, evaluation). Each skill reads its inputs from it and writes its outputs to it. The naive copy is written once, with its source reference. ad writes after each stressor. | all | S14, S23, S30, S39, S46 |
| C05 | Reference script for counts and similarities, in the skill directory. Without a code tool: count by hand, compare only pairs with ≥ 3 shared stressors, recount the top results. | fhc | S26, S33 |
| C06 | Degenerate mapping check: if all pairs or no pairs are coupled, or one element has most stressors, report that the mapping is too coarse or too fine. Return to mapping. Do not report groups. | fhc | S37 |
| C07 | Fixed split: each stressor is in exactly one set. The split is recorded before ad starts. ad does not start without a split, and offers to make one. ed checks that the sets are disjoint and reports where the test stressors came from. | gs, ad, ed | S43, S60 |
| C08 | Unique element IDs. If names collide, add a qualifier and record the mapping. | gs, fhc | S53 |
| C09 | Ri checks: N ≤ S, R ≤ S, each stressor counted at most once for each design, −1 ≤ Ri ≤ 1. | ed | S58 |

## Consolidation

- C02 and C07 become files in the C04 run record: `criteria.md`, and a `set` column in the stressor table.
- Finding 1 (`ad`–`ed`): the shared state moves to the run record. The run record owns it. Neither skill defines survival alone.
- Finding 2 (`affects`–`groups`): C06 and C08 protect the groups from a bad mapping.
- Two-way `ed` ↔ `gs`: with C07, ed generates test stressors only if no split exists. It reports that provenance.

## Pass 2

All 45 training stressors applied to the consolidated design. S25 still fails. No other failures. No new changes. Stop.
