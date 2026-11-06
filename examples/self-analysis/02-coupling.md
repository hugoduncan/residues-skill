# Step 2: find-hidden-coupling

Input: 45 training stressors from [stressors.tsv](stressors.tsv). Counts from [analyse.py](analyse.py). Limits: similarity ≥ 0.5, shared ≥ 3.

## Findings

1. **`ad` and `ed` have hidden coupling** (11 shared stressors, similarity 0.52). The design connects them only through the naive and adapted designs. The shared stressors (S11, S40, S39, S60, S22) show the real connection: both skills depend on the survival criteria, the essential functions, the naive copy and the test marking. No element owns this shared state. Each skill defines "survive" separately.
2. **`affects` and `groups` have hidden coupling** (4 shared, 0.57). The groups depend only on the affects mapping. A coarse or wrong mapping (S37, S53) gives wrong groups with no warning.
3. **`desc` and `harness`** (4 shared, 0.57). Known coupling.
4. **Near pairs:** `essentials`–`survive` (0.43) confirms finding 1. `design-in`–`elements` (0.44): large or unclear designs damage the element list.
5. **Dangerous stressors:** S29 (harness renames skills), S28 (harness loads only descriptions), S30 (no context between steps), S21 (token cost), S50 (10 minutes).

## Dependency findings

- Two-way: `fhc` ↔ `gs` (fhc generates stressors if they are missing). `ed` ↔ `gs` (ed generates test stressors if they are missing). The second path lets test stressors come into existence after adaptation.
- Two-way: `ad` ↔ `adapted` (recheck loop). `user` ↔ `decisions`.
- Unsupported links: none found.

## Boundary candidates

| Candidate | Elements | Stressors |
|---|---|---|
| One owner for shared run state: criteria, test marking, naive copy | ad, ed, essentials, survive, test-mark, naive | S11, S14, S30, S39, S40, S60 |
| Validate the affects mapping before grouping | affects, groups, elements | S37, S53 |
| Fix the test set before adaptation. Restrict `ed` → `gs`. | test-mark, ed, gs | S43, S60 |

## Raw output

### Vulnerable elements

| Element | Count | Stressors |
|---|---|---|
| ad | 16 | S10, S11, S13, S19, S20, S21, S22, S27, S28, S29, S39, S40, S46, S50, S51, S60 |
| ed | 16 | S04, S11, S12, S13, S19, S21, S22, S28, S29, S39, S40, S43, S49, S50, S58, S60 |
| fhc | 13 | S13, S19, S21, S23, S24, S26, S28, S29, S33, S36, S37, S50, S53 |
| gs | 12 | S05, S10, S13, S19, S20, S21, S28, S29, S34, S50, S55, S56 |
| context | 9 | S05, S21, S23, S30, S34, S45, S46, S50, S51 |
| user | 9 | S01, S03, S04, S14, S17, S42, S47, S50, S56 |
| repo | 8 | S01, S03, S13, S19, S25, S29, S42, S47 |
| stressors | 8 | S14, S20, S30, S31, S42, S43, S55, S59 |
| design-in | 7 | S05, S10, S17, S32, S34, S54, S56 |
| elements | 6 | S05, S32, S34, S36, S53, S54 |
| essentials | 6 | S10, S11, S30, S40, S49, S54 |
| groups | 6 | S30, S31, S33, S37, S53, S59 |
| harness | 6 | S01, S17, S25, S28, S29, S45 |
| model | 6 | S17, S21, S23, S27, S32, S45 |
| naive | 6 | S12, S14, S30, S39, S46, S49 |
| ri | 6 | S04, S31, S39, S43, S58, S59 |
| adapted | 5 | S12, S22, S46, S49, S51 |
| affects | 5 | S31, S36, S37, S53, S59 |
| code-tool | 5 | S23, S24, S26, S33, S45 |
| decisions | 5 | S04, S11, S14, S20, S47 |
| desc | 5 | S01, S03, S25, S28, S29 |
| test-mark | 5 | S14, S30, S43, S58, S60 |
| survive | 4 | S10, S11, S27, S40 |
| gen-tables | 2 | S54, S55 |
| limits | 2 | S33, S37 |

### Dangerous stressors (≥ 5 elements)

| ID | Elements | Stressor |
|---|---|---|
| S29 | 7 | The harness renames skills on load. "Related skills" names do not match. |
| S21 | 6 | Token cost increases 10 times. |
| S28 | 6 | The harness loads only the description, never the skill body. |
| S30 | 6 | Each skill runs in a new session. No context passes between steps. |
| S50 | 6 | A user must deliver results in 10 minutes. |
| S10 | 5 | A user wants to stress a running production system, not a design. |
| S11 | 5 | A user disagrees with every survival decision. |
| S13 | 5 | The skill author leaves. Nobody maintains the skills. |
| S14 | 5 | A team of five shares the work. Each person runs a different step. |
| S19 | 5 | A licence change forbids redistribution of the skill text. |

### Coupled pairs (similarity ≥ 0.5, shared ≥ 3)

| A | B | Shared | Similarity | In design | Stressors |
|---|---|---|---|---|---|
| affects | groups | 4 | 0.57 | no (hidden) | S31, S37, S53, S59 |
| desc | harness | 4 | 0.57 | yes | S01, S25, S28, S29 |
| ad | ed | 11 | 0.52 | no (hidden) | S11, S13, S19, S21, S22, S28, S29, S39, S40, S50, S60 |

### Near pairs (similarity ≥ 0.4, shared ≥ 3, below limit)

| A | B | Shared | Similarity | In design |
|---|---|---|---|---|
| ad | gs | 8 | 0.40 | no (hidden) |
| desc | repo | 4 | 0.44 | no (hidden) |
| design-in | elements | 4 | 0.44 | no (hidden) |
| essentials | survive | 3 | 0.43 | no (hidden) |

### Elements with no training stressor

none
