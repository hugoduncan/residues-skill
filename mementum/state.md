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

Independent evaluation: `.psi/workflows/evaluate-design.md` runs evaluate-design in a fresh session (delegate). After adding a workflow file, reload with /delegate-reload.

Run record: one directory, fixed files (design.md, elements.tsv, stressors.tsv with `set`, connections.tsv, coupling.md, criteria.md, naive.md, adaptation.md, adapted.md, evaluation.md). First line: `# run: <id> | date: <date> | skill: <name>`.

## Decisions

- Frontmatter: agentskills.io spec plus top-level `lambda` (for psi). `skills-ref validate` reports it.
- Split only when the user plans to adapt. adapt-design requires a split. Split after coverage. No stressors after the split. After the split, each element with stressors needs a training stressor, else split again with the next seed.
- No file access → output files as fenced blocks.
- Tie (neither survives, equal) counts for neither design. Source does not define ties.
- adapt-design applies the criteria exceptions (for example a clear failure that names the fix) before "no", and names the lost function.
- Test stressors used in a later pass: `# retired: <ids> | date:` line in stressors.tsv; `set` unchanged. evaluate-design excludes them.
- evaluate-design notes graded gains (for example an earlier fallback) but does not count them.
- Coupling defaults 0.5 / 3. If no hidden pairs: sensitivity runs at similarity 0.35 and 0.3, reported separately.
- evaluate-design reports Ri limits. S − N < 5 → Ri cannot show an effect (heuristic). Recommend ~200 stressors for a well-analysed design. See mementum/memories/ri-ceiling.md.
- Each SKILL.md stays ≤ 1000 words (ramora). Trim, do not split.

## Next

None.

## Related

- munera/plan.md — task order
- ramora/INDEX.md — document index
- mementum/memories/ — insights
- README.md
