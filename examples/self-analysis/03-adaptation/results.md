# Step 3: adapt-design — Stressor results

Index: [../03-adaptation.md](../03-adaptation.md)

## Essential functions

- EF1: Produce a broad stressor list, with affected elements, for a given design.
- EF2: Identify vulnerable elements and coupled groups from that list.
- EF3: Produce an adapted design. Each change traces to stressors. The naive design stays unchanged.
- EF4: Produce a fair comparison (Ri) of the naive and the adapted design, on stressors not used during adaptation.

Acceptable effort: the user recovers with one clarification or one rerun of one step. A silently wrong result does not survive.

## Stressor results (pass 1)

| ID | Effect | Survives | Change |
|---|---|---|---|
| S01 | Fewer users. Skills still work when used. | yes | |
| S03 | Same as S01. | yes | |
| S04 | Ri is in the output. | yes | |
| S05 | Context overflows during gs step 1. Silent truncation. | no | C01 |
| S10 | User describes the system. gs asks if unclear. | yes | |
| S11 | Survival defined in two skills. Recovery needs a rerun of ad and ed. | no | C02 |
| S12 | ed has no rule for a missing naive design. It can use the adapted design as the naive one. | no | C03 |
| S13 | No maintenance. Skills still work. | yes | |
| S14 | Test marks, naive copy and criteria exist only in one conversation. | no | C04 |
| S17 | Model choice is outside the skills. | yes | |
| S19 | Distribution only. | yes | |
| S20 | gs allows extra columns. Probability can be recorded, not used. | yes | |
| S21 | User gives a smaller quantity. | yes | |
| S22 | User stops after one pass. | yes | |
| S23 | All tables stay in context. Overflow. | no | C04 (reuse) |
| S24 | One code call does all counts. | yes | |
| S25 | Skills do not load. Frontmatter has non-standard fields. | no | open decision D1 |
| S26 | No tool, and fhc says "do not calculate by hand". No path. | no | C05 |
| S27 | Different changes. Still traceable. | yes | |
| S28 | The lambda line carries the core procedure. | yes | |
| S29 | Each skill states its own input. It works alone. | yes | |
| S30 | State lost between sessions. | no | C04 (reuse) |
| S31 | Tables stay readable as text. | yes | |
| S32 | gs asks if unclear. | yes | |
| S33 | Agent writes a new script each run. A bug gives wrong groups. | no | C05 (reuse) |
| S34 | Same as S05. | no | C01 (reuse) |
| S36 | fhc step 1 normalises names. | yes | |
| S37 | One group with all elements. No warning. | no | C06 |
| S39 | Naive copy has no protection. | no | C04 (reuse) |
| S40 | ed asks for criteria again. They can differ from ad. | no | C02 (reuse) |
| S42 | Storage is the choice of the user. | yes | |
| S43 | ed cannot see when test stressors came into existence. Biased Ri. | no | C07 |
| S45 | Lower quality. Outside the skills. | yes | |
| S46 | Progress lost. | no | C04 (reuse) |
| S47 | Outside the skills. | yes | |
| S49 | ed evaluates designs, not the current system. | yes | |
| S50 | User gives a smaller quantity. | yes | |
| S51 | Stop after three passes. | yes | |
| S53 | "Merge synonyms" merges different elements with the same name. | no | C08 |
| S54 | Categories are general. | yes | |
| S55 | Absurd events are valid. | yes | |
| S56 | gs asks if unclear. | yes | |
| S58 | No explicit check of counts. | no | C09 |
| S59 | Order does not change counts. | yes | |
| S60 | No check that test and training sets are disjoint. | no | C07 (reuse) |
