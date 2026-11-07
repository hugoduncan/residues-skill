# State

Working memory. Read first in each session. Update after each significant change.

## Project

Residues Skill. Agent skills based on Residuality Theory (Barry M. O'Reilly).
Source paper: https://doi.org/10.1016/j.procs.2022.03.084. Ri = (R − N) / S, verified from the 2022 PDF (p. 644).

- Published: https://github.com/hugoduncan/residues-skill (public, EPL-2.0). Install: `npx skills add hugoduncan/residues-skill`.
- Protocols: mementum, munera, ramora. No open tasks.
- Background: ramora/stressors.md, ramora/residues.md (O'Reilly 2022 via pragsmike/cyberneutics, O'Reilly 2020).

## Skills

Self-contained, no theory needed. Pipeline order:

1. skills/generate-stressors: design → stressors + affected elements → coverage → optional training/test split.
2. skills/find-hidden-coupling: stressor × element matrix → vulnerable, dangerous, coupled groups. Script: scripts/coupling.py (+ test_coupling.py).
3. skills/adapt-design: training stressors → smallest changes → consolidate.
4. skills/evaluate-design: test stressors on naive vs adapted → Ri, Ri limits, regressions.

Run record: one directory, fixed files (design.md, elements.tsv, stressors.tsv with `set`, connections.tsv, coupling.md, criteria.md, naive.md, adaptation.md, adapted.md, evaluation.md). First line: `# run: <id> | date: <date> | skill: <name>`.

## Decisions

- Frontmatter: agentskills.io spec plus top-level `lambda` (for psi). `skills-ref validate` reports it.
- Split only when the user plans to adapt. adapt-design requires a split. Split after coverage. No stressors after the split.
- No file access → output files as fenced blocks.
- Tie (neither survives, equal) counts for neither design. Source does not define ties.
- Coupling defaults 0.5 / 3. If no hidden pairs: sensitivity runs at similarity 0.35 and 0.3, reported separately.
- evaluate-design reports Ri limits. S − N < 5 → Ri cannot show an effect (heuristic). See mementum/memories/ri-ceiling.md.
- Each SKILL.md stays < 1000 words (ramora).

## Examples

- examples/self-analysis: pipeline on its own design. Ri = 0.27 (15 test stressors). Changes C01–C09 applied.
- examples/value-type: run value-type-r1 on ~/projects/hugoduncan/value-type (commit 5073893f). 73 stressors (55/18), 8 changes, Ri = 0.00, ceiling 0.11, no regressions. Feedback applied to skills and README ("Limits").
  - Inputs come from examples/value-type/build_inputs.py. Edit the script, not the TSV files.
  - evaluate-design ran in a fresh session through .psi/workflows/evaluate-design.md (delegate). After adding a workflow file, reload with /delegate-reload.

## Next

- Self-analysis second pass with S18, S35, S41, S44, S52 (repeatability, duplicate IDs, prompt injection, malicious fork, skill versions).
- value-type: second pass with S38, S58 as training stressors (silent JVM defects), or repeated splits.

## Related

- munera/plan.md — task order
- ramora/INDEX.md — document index
- mementum/memories/ — insights
- README.md
