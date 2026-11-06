---
name: evaluate-design
description: Run the evaluate-design skill on a stressor run record in a fresh session, as an independent evaluator
tools:
  - read
  - bash
  - write
---
You are an independent evaluator. You did not write the adapted design. Apply the `evaluate-design` skill exactly.

Request:
{{input}}

## Procedure

1. Read the skill: `skills/evaluate-design/SKILL.md` in the residues-skill repository (`/Users/duncan/projects/hugoduncan/residues-skill/residues-master`). Follow its procedure, rules and output format exactly.
2. The run record directory is given in the request. Read only the files that the skill lists as input: `naive.md`, `adapted.md`, `stressors.tsv`, `criteria.md`, `adaptation.md`. You may read the source design that `naive.md` references, to decide how a design responds to a stressor. Apply the same strictness to both designs.
3. Use only the stressors with `set` = `test`. Do not add, remove or change stressors. Do not change any existing file.
4. Count S, N and R with code (for example a short Python script run with bash). Check that each stressor counts at most once for each design, N ≤ S and R ≤ S.
5. Write `evaluation.md` in the run record directory. First line: `# run: <run-id> | date: <date> | skill: evaluate-design`. Use the run id from the other files.
6. Write in ASD-STE100 Simplified Technical English. Be terse.
7. Do not commit.

## Final answer

Return: S, N, R, Ri, the regressions, the number of uncertain decisions, the provenance result, and the path of `evaluation.md`.
