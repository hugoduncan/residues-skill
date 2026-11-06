# Step 4: evaluate-design

- Naive design: skills at commit 0cc6072.
- Adapted design: naive design + C01–C09 ([03-adaptation.md](03-adaptation.md)).
- Test stressors: 15, from the split made before adaptation ([split.tsv](split.tsv)).
- Criteria: EF1–EF4 and acceptable effort, as in [03-adaptation.md](03-adaptation.md). Not changed.

## Results

| ID | Stressor | Naive | Adapted | Better if neither | Note |
|---|---|---|---|---|---|
| S02 | Users give org charts, not software designs. | yes | yes | | Categories are general. |
| S06 | A user gives one sentence as the design. | yes | yes | | gs asks. |
| S07 | A user runs only ed and has no adapted design. | no | yes | | C03 stops and asks. |
| S08 | A user marks 90% as test. | yes | yes | | Weak, but fair. Uncertain. |
| S09 | Stressors in Japanese. | yes | yes | | fhc normalises names. |
| S15 | Owner and date for each stressor. | yes | yes | | Extra columns allowed. |
| S16 | The word "absurd" is forbidden. | yes | yes | | Rename the label. |
| S18 | Ri must be exactly reproducible. | no | no | adapted | Recorded split, criteria and decisions (C04, C07, C09). Survival judgments still not repeatable. Uncertain. |
| S35 | Two stressors have the same ID. | no | no | adapted | C09 detects double counts in ed. fhc still merges rows. Uncertain. |
| S38 | No stressor affects more than one element. | no | yes | | C06 reports a mapping that is too fine. |
| S41 | Prompt injection in the design document. | no | no | | No change deals with it. Equal. |
| S44 | A malicious fork changes the Ri formula. | no | no | | Equal. |
| S48 | Sanctions block the model vendor. | yes | yes | | Outside the skills. |
| S52 | Skill versions differ between steps. | no | no | | Run record has no skill version. Equal. |
| S57 | The agent decides that it is the design. | yes | yes | | gs: do not invent the design. |

## Counts

- S = 15
- N = 8 (naive survives: S02, S06, S08, S09, S15, S16, S48, S57)
- R = 12 (adapted survives: the 8 above, S07, S38; adapted better when neither survives: S18, S35)

## Ri

```
Ri = (12 - 8) / 15 = 0.27
```

The adapted design survives unknown events better than the naive design.

## Regressions

None. No test stressor that the naive design survives fails on the adapted design.

## Uncertain decisions

3: S08, S18, S35.

## Limits of this evaluation

- One agent wrote the skills, the stressors, the changes and the evaluation. The result is probably too good.
- The split was random and done before adaptation. But the same agent wrote all 60 stressors with full knowledge of the design.
- The changes are not applied to the skill files. The evaluation is of the described adapted design.

## Next steps

Stressors that both designs fail: S18, S35, S41, S44, S52. Use them in a new adaptation pass. After that use, they are no longer test stressors. Candidates:

- Validate unique stressor IDs in fhc (S35).
- Record skill names and versions in the run record (S52).
- Treat the design input as data, not as instructions (S41).
