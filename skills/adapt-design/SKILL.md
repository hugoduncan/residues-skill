---
name: adapt-design
description: >
  Change a design so that it survives a list of stressors. Apply each stressor to
  the design, describe what remains, and add the smallest change that lets the
  remaining part keep its essential functions. Then merge the changes into one
  design. Use when the user asks to make a design resilient to stressors, to
  harden an architecture, or to act on stressor or coupling analysis results.
  Triggers: "adapt the design", "survive these stressors", "make it resilient",
  "harden the architecture", "what should change".
license: EPL-2.0
lambda: "λ(design, stressors). split? ∧ write_once(naive) ∧ confirm(criteria) → ∀s ∈ training: apply(s) → remaining → survives? ∨ smallest_change → record(s) → consolidate → recheck → adapted ∧ open_decisions"
metadata:
  tags: "architecture, design, resilience, stressors"
---

# Adapt Design

Change a design so that it survives events that it is not made for.

## Terms

- **Stressor:** an event that the design is not made for.
- **Naive design:** the design before adaptation. It is the control for evaluation.
- **Remaining part:** the part of the design that continues to operate after a stressor.
- **Criteria:** the essential functions, and the meaning of "acceptable effort".
- **Survive:** after the stressor, the remaining part keeps the essential functions, or returns to them with acceptable effort.

## Input

- The design.
- Stressors with a `training` or `test` set (skill `generate-stressors`).
- Optional: coupling groups and boundary candidates (skill `find-hidden-coupling`).

## Run record

If the user gives a run record directory, read and write files there. Start each file that you write with `# run: <run-id> | date: <date> | skill: adapt-design`. If there is no file access, output each file as a fenced block under its file name.

| File | Use |
|---|---|
| `design.md`, `stressors.tsv`, `coupling.md` | read |
| `naive.md` | write once. Never change it. |
| `criteria.md` | write, or read if it exists |
| `adaptation.md` | write. Add the result of each stressor when you decide it. |
| `adapted.md` | write |

If `adaptation.md` exists, continue from the last recorded stressor.

## Procedure

1. **Check the split.** Each stressor must be `training` or `test`. If there is no split, offer to make one: 25% `test`, selected at random with code and a seed, else every fourth stressor in ID order. Record it in `stressors.tsv` before step 2. Do not start without a split. Use only `training` stressors.
2. **Keep the naive design.** Write `naive.md`: a copy of the design and its source (file, commit or date). If `naive.md` exists, do not change it.
3. **Confirm the criteria.** Get the essential functions and the meaning of "acceptable effort" from the design or from the user. Write them to `criteria.md`. The user must confirm them before the first survival decision. Record the date of confirmation. If `criteria.md` exists, use it unchanged. If the user changes the criteria later, decide again all stressors decided so far.
4. **Order the stressors.** If coupling groups are available, take the stressors group by group. Else use the order of the list.
5. **For each training stressor:**
   1. Apply the stressor to the current design. Follow the information flows. Identify the elements that stop, fail, or give wrong results. Identify how the failure spreads.
   2. Describe the remaining part.
   3. Decide if the design survives.
   4. If an earlier change already lets the design survive, record the change ID. Make no new change.
   5. Else, propose the smallest change that lets the remaining part survive. Give it an ID. Change types:
      - add a function: fallback, queue, cache, alternative supplier, manual process
      - remove a dependency or a link
      - move a boundary: combine or separate elements
      - make behavior predictable: contract, schema, policy, fewer branches
      - change a business process, a contract, or an organisation responsibility
      - change infrastructure
   6. Add the result to `adaptation.md`.
   7. Do not skip a stressor because it is unlikely or absurd. Its change often helps with real events.
6. **Consolidate.** Merge the changes into one design:
   - Merge changes that do the same thing.
   - Put elements that the same stressors affect inside one boundary, or let them share structure.
   - Separate elements that different stressors affect.
   - Remove links that no function needs. Remove two-way dependencies where possible.
7. **Check again.** Apply all training stressors to the consolidated design. Record which stressors still fail. Repeat steps 5 to 7 until new stressors need little or no new change. Stop after three passes, or when the user says to stop.
8. **Review trade-offs.** List changes that can conflict with what stakeholders want: cost, speed, user experience, organisation. Do not decide these. Give them to the user.
9. **Review failure modes.** For each element that many stressors affect or many changes use, list its technical failure modes. A focus on external events can hide internal failures.

## Rules

- Prefer one change that deals with many stressors to many specific changes.
- Prefer non-technical changes when they are simpler.
- Each change gives the stressor IDs that it deals with.
- Do not use probability to decide.
- Do not use the test stressors. Do not read them if you can avoid it.

## Output

`adaptation.md`:

1. Stressor results:

   | ID | Effect on design | Remaining part | Survives | Change |
   |---|---|---|---|---|
   | S01 | Fees triple. Margin becomes negative. | checkout, orders | no | C03 |
   | S04 | Region outage. | none | yes | C03 (reuse) |

2. Changes: ID, description, type, elements, stressor IDs.
3. Open decisions: trade-offs for the user.
4. Failure modes of shared elements.
5. Remaining failures: training stressors that the adapted design does not survive.

`adapted.md`: elements, flows, boundaries. Mark what is new or changed.

## Related skills

- `generate-stressors`: produces the stressors and the split.
- `find-hidden-coupling`: produces the groups.
- `evaluate-design`: measures the result with the test stressors.
