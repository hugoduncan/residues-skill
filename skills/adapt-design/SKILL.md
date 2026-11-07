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
lambda: "λ(design, stressors). split? ∧ write_once(naive) ∧ confirm(criteria) → ∀s ∈ training: apply(s) → remaining → survives?(criteria ∧ exceptions) ∨ smallest_change → record(s) → consolidate → recheck → adapted ∧ open_decisions"
metadata:
  tags: "architecture, design, resilience, stressors"
---

# Adapt Design

Change a design so that it survives events that it is not made for.

## Terms

- **Stressor:** an event that the design is not made for.
- **Naive design:** the design before adaptation; the control for evaluation.
- **Remaining part:** the part that still operates after a stressor.
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
| `design.md`, `coupling.md` | read |
| `stressors.tsv` | read. Add only `# retired:` lines (step 1). |
| `naive.md` | write once. Never change it. |
| `criteria.md` | write, or read if it exists |
| `adaptation.md` | write. Add the result of each stressor when you decide it. |
| `adapted.md` | write |

If `adaptation.md` exists, continue from the last recorded stressor.

## Procedure

1. **Check the split.** Each stressor must be `training` or `test`. If there is no split, offer to make one: 25% `test`, random with code and a seed, else every fourth ID. Record it in `stressors.tsv` before step 2. Do not start without a split. Use only `training` stressors.
   - To use test stressors in a new pass (`evaluate-design` next steps), add `# retired: <ids> | date: <date>` to `stressors.tsv`. Do not change their `set`.
2. **Keep the naive design.** Write `naive.md`: a copy of the design and its source (file, commit or date). If it exists, do not change it.
3. **Confirm the criteria.** Get the criteria from the design or from the user. Write `criteria.md`. The user confirms them before the first decision. Record the date. If `criteria.md` exists, use it unchanged. If the criteria change later, decide all earlier stressors again.
4. **Order the stressors.** If coupling groups are available, take the stressors group by group. Else use the order of the list.
5. **For each training stressor:**
   1. Apply the stressor to the current design. Follow the flows. Find the elements that stop, fail or give wrong results, and how the failure spreads.
   2. Describe the remaining part.
   3. Decide if the design survives. Apply the criteria and their exceptions exactly (for example, a clear failure that names the fix). For "no", name the lost function.
   4. If an earlier change already lets it survive, record only that change ID.
   5. Else, propose the smallest change that lets the remaining part survive. Give it an ID. Types:
      - add a function: fallback, queue, cache, alternative supplier, manual process
      - remove a dependency or a link
      - move a boundary: combine or separate elements
      - make behavior predictable: contract, schema, policy, fewer branches
      - change a business process, a contract, or an organisation responsibility
      - change infrastructure
   6. Add the result to `adaptation.md`.
   7. Do not skip unlikely or absurd stressors. Their changes often help with real events.
6. **Consolidate.** Merge the changes into one design:
   - Merge changes that do the same thing.
   - Put elements that the same stressors affect inside one boundary, or let them share structure.
   - Separate elements that different stressors affect.
   - Remove links that no function needs. Remove two-way dependencies where possible.
7. **Check again.** Apply all training stressors to the consolidated design. Record the stressors that still fail. Repeat steps 5 to 7 until little new change is needed, for at most three passes or until the user stops.
8. **Review trade-offs.** List changes that can conflict with stakeholder goals: cost, speed, user experience, organisation. Give them to the user to decide.
9. **Review failure modes.** For each element that many stressors affect or many changes use, list its technical failure modes. A focus on external events can hide internal failures.

## Rules

- Prefer one change that deals with many stressors to many specific changes.
- Prefer simpler non-technical changes.
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
