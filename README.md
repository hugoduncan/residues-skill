# Residues Skill

Agent skills to stress a software design with unexpected events, find hidden coupling, change the design, and measure the result.

## Problem

A software system operates in a business environment that is not predictable. Events occur that the design is not made for. Requirements and risk analysis examine only a small set of likely futures. Parts of a design that the same event affects are coupled, but the design does not show this coupling. It becomes visible only when the event occurs.

## Approach

The skills apply residual analysis from Residuality Theory (Barry M. O'Reilly). They do not require knowledge of the theory.

1. Generate many random stressors for the design. A stressor is an event that the design is not made for. Probability is not used. Absurd events are included.
2. Map each stressor to the design elements that it affects. Elements that the same stressors affect are coupled.
3. Apply each stressor to the design. Add the smallest change that lets the design keep its essential functions. Merge the changes.
4. Apply stressors that were not used in step 3 to the original and to the changed design. Compare the results with the index Ri = (R − N) / S.

| Skill | Input | Output |
|---|---|---|
| `generate-stressors` | design | stressors, affected elements, optional training/test split |
| `find-hidden-coupling` | stressors, design | vulnerable elements, dangerous stressors, coupled groups, boundary candidates |
| `adapt-design` | design, training stressors | changes, adapted design, open decisions |
| `evaluate-design` | original design, adapted design, test stressors | Ri, regressions |

Each skill works alone. The skills share data through a run record: a directory with fixed file names.

## Status

Experimental. The skills are tested once, on their own design (see [examples/self-analysis](examples/self-analysis/)). They are not yet tested on a real system design. File formats and skill text can change without backward compatibility.

## AI usage

An AI agent wrote the skills, the script, the documentation and the example, under human direction and review. The theory summaries come from the papers listed below.

## Installation

Requirements:

- An agent harness that loads skills from `SKILL.md` files with YAML frontmatter.
- Python 3, for the counting script of `find-hidden-coupling`. Without Python, the skill uses a manual method.

Copy the skill directories into the skill directory of your harness:

```sh
git clone <repository-url> residues-skill
cp -r residues-skill/skills/* <harness-skill-directory>/
```

Examples of skill directories: `~/.claude/skills/` (Claude Code), `~/.psi/agent/skills/` or `.psi/skills/` (psi).

## Usage

Ask the agent for each step. Give the design and a run record directory.

```text
Generate stressors for the design in docs/architecture.md.
Use the run record stressor-runs/r1. I plan to adapt and evaluate the design.

Find hidden coupling in stressor-runs/r1.

Adapt the design in stressor-runs/r1.

Evaluate the design in stressor-runs/r1.
```

`adapt-design` asks you to confirm the essential functions before it decides if the design survives a stressor. It gives trade-offs to you. It does not decide them.

To reduce bias, run `evaluate-design` in a new session, or let a different person run it.

To run the counting script directly:

```sh
python3 skills/find-hidden-coupling/scripts/coupling.py stressor-runs/r1
```

Details of each step are in the `SKILL.md` file of each skill.

## Background

- [ramora/stressors.md](ramora/stressors.md) and [ramora/residues.md](ramora/residues.md): summaries of the concepts.
- O'Reilly, B. M. (2022). Residuality Theory, random simulation, and attractor networks. Procedia Computer Science 201: 639–645. https://doi.org/10.1016/j.procs.2022.03.084
- O'Reilly, B. M. (2020). An introduction to residuality theory: Software design heuristics for complex systems. Procedia Computer Science 170: 875–880. https://doi.org/10.1016/j.procs.2020.03.120
