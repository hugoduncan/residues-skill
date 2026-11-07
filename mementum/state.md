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
  - Pass 3 (after evaluation): S38, S58 used for training → C09–C11 (value-class switch, semantic self-check, forced-JIT row). S58 survives, S38 partial. Not evaluated. stressors.tsv not changed.
  - Inputs come from examples/value-type/build_inputs.py. Edit the script, not the TSV files.
  - evaluate-design ran in a fresh session through .psi/workflows/evaluate-design.md (delegate). After adding a workflow file, reload with /delegate-reload.
- examples/value-type-r2: same design, 124 new stressors (112 + 12 from coverage, then split 93/31), updated skills. Coupling: 0 hidden at defaults, 1 at 0.3 (cap-probe–loader, shared DynamicClassLoader). 11 changes. Ri = 0.00, max 0.10, no regressions. Inputs from build_inputs.py (reads r1 elements/connections).

## Skill feedback from r2 (not yet applied)

- More stressors do not raise the Ri maximum: naive survival ≈ 90% in r1 and r2. S − N ≥ 5 needs ~50 test stressors (~200 total). The memory ri-ceiling already says this.
- Coverage vs split: coverage added 2 stressors for expansion-transfer; the random split put both in test → 0 training. Candidate: check training coverage after the split, or stratify.
- Adapter stricter than evaluator: criteria count "clear failure that names the fix" as survival; adaptation missed it for S039/S097 (naive already says "Fix: use Clojure 1.12"). Candidate: adapt-design checks the criteria exceptions before a "no".
- Binary survival hides graded gains (evaluator: earlier fallback, smaller fix boundary in 5 test stressors).
- No mechanism to record test stressors used in a later pass (r1 pass 3).
- r1 adaptation S34 code fact was wrong: the field probe throws when NullRestricted is ignored.

## Next

- Self-analysis second pass with S18, S35, S41, S44, S52 (repeatability, duplicate IDs, prompt injection, malicious fork, skill versions).
- Decide on the r2 skill feedback above.
- value-type-r2: optional pass with S073, S099 (both designs fail).

## Related

- munera/plan.md — task order
- ramora/INDEX.md — document index
- mementum/memories/ — insights
- README.md
