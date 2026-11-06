# Self-analysis: the stressor skills applied to themselves

The four skills in `skills/` run on their own design.

| Step | Skill | File |
|---|---|---|
| 0 | design under analysis | [00-design.md](00-design.md) |
| 1 | generate-stressors | [01-stressors.md](01-stressors.md), [stressors.tsv](stressors.tsv), [split.tsv](split.tsv) |
| 2 | find-hidden-coupling | [02-coupling.md](02-coupling.md), [analyse.py](analyse.py) |
| 3 | adapt-design | [03-adaptation.md](03-adaptation.md) (index), [03-adaptation/](03-adaptation/) |
| 4 | evaluate-design | [04-evaluation.md](04-evaluation.md) |

Result: 9 changes (C01–C09), 4 open decisions, Ri = 0.27 on 15 test stressors.

Reproduce the counts: `python3 analyse.py split`, then `python3 analyse.py`.
