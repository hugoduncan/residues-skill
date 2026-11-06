# State

Working memory. Read first in each session. Update after each significant change.

## Project

Residues Skill. An agent skill based on Residuality Theory (Barry M. O'Reilly, 2022).
Source paper: https://doi.org/10.1016/j.procs.2022.03.084

## Current

- Protocols initialised: mementum, munera, ramora.
- Ramora documents: ramora/stressors.md, ramora/residues.md. Sources: O'Reilly 2022 (via pragsmike/cyberneutics), O'Reilly 2020.
- Ri = (R - N) / S. Verified from the 2022 PDF (equation image, p. 644).
- Skills (self-contained, no theory needed), pipeline order:
  - skills/generate-stressors: design → stressors + affected elements
  - skills/find-hidden-coupling: stressor × element matrix → vulnerable, dangerous, coupled groups
  - skills/adapt-design: apply training stressors → smallest changes → consolidate
  - skills/evaluate-design: test stressors on naive vs adapted → Ri = (R - N) / S
- Decision: evaluate-design counts a tie (neither survives, equal) for neither design. Source does not define ties.
- No open tasks.

## Next

- Test the skill pipeline end to end on a sample design.

## Related

- munera/plan.md — task order
- ramora/INDEX.md — document index
- README.md
