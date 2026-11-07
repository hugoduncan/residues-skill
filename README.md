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

Experimental. The skills are tested on two designs:

- Their own design: [examples/self-analysis](examples/self-analysis/). Ri = 0.27.
- A real library, [value-type](https://github.com/hugoduncan/value-type), in two runs:
  - [examples/value-type](examples/value-type/): 73 stressors. Ri = 0.00, no regressions. The original design survives 16 of 18 test stressors, so Ri can be at most 0.11.
  - [examples/value-type-r2](examples/value-type-r2/): 124 stressors, with the skills after the r1 feedback. Ri = 0.00, no regressions, maximum 0.10. More stressors did not raise the maximum.

File formats and skill text can change without backward compatibility.

## AI usage

An AI agent wrote the skills, the script, the documentation and the example, under human direction and review. The theory summaries come from the papers listed below.

## Installation

Requirements:

- An agent harness that loads skills from `SKILL.md` files with YAML frontmatter.
- Python 3, for the counting script of `find-hidden-coupling`. Without Python, the skill uses a manual method.

### With the skills CLI

Install all four skills with the [skills CLI](https://skills.sh):

```sh
npx skills add hugoduncan/residues-skill
```

Install one skill only:

```sh
npx skills add hugoduncan/residues-skill --skill generate-stressors
```

Add `-g` to install for all projects. List the skills without installing them:

```sh
npx skills add hugoduncan/residues-skill --list
```

### Manual

Copy the skill directories into the skill directory of your harness:

```sh
git clone https://github.com/hugoduncan/residues-skill.git
cp -r residues-skill/skills/* <harness-skill-directory>/
```

Examples of skill directories: `~/.claude/skills/` (Claude Code), `~/.psi/agent/skills/` or `.psi/skills/` (psi).

### Frontmatter

The skills follow the [Agent Skills specification](https://agentskills.io), with one addition: a `lambda` field, which psi uses. Other harnesses ignore it. Strict validators, for example `skills-ref validate`, report it as an unexpected field.

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

### Limits

- **Coupling limits.** `find-hidden-coupling` marks a pair as coupled at similarity ≥ 0.5 and ≥ 3 shared stressors. A design that shows its connections well can have no hidden pairs at these limits. The skill then runs again at similarity 0.35 and 0.3, and reports those pairs separately.
- **Ri limits.** Ri can be at most (S − N) / S. If the original design survives most test stressors, Ri cannot show an effect. `evaluate-design` reports the limits. For a design with a strong risk analysis, generate more stressors (about 200), or repeat the split and the adaptation, and report the range of Ri.
- **Order.** `generate-stressors` adds stressors in the coverage step, and splits after that. Do not add stressors after the split. After the split, each element must have a training stressor.
- **Later passes.** `adapt-design` can use test stressors that both designs fail in a new pass. It marks them with a `# retired:` line in `stressors.tsv`, and `evaluate-design` does not use them.

## Background

- [ramora/stressors.md](ramora/stressors.md) and [ramora/residues.md](ramora/residues.md): summaries of the concepts.
- O'Reilly, B. M. (2022). Residuality Theory, random simulation, and attractor networks. Procedia Computer Science 201: 639–645. https://doi.org/10.1016/j.procs.2022.03.084
- O'Reilly, B. M. (2020). An introduction to residuality theory: Software design heuristics for complex systems. Procedia Computer Science 170: 875–880. https://doi.org/10.1016/j.procs.2020.03.120

## License

Copyright © 2026 Hugo Duncan.

Distributed under the [Eclipse Public License 2.0](LICENSE). No Secondary Licenses apply.
