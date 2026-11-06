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
lambda: "λ(design, stressors). keep(naive) → ∀s ∈ training: apply(s) → remaining → survives? ∨ smallest_change → consolidate(changes) → recheck → adapted_design ∧ open_decisions"
metadata:
  tags: ["architecture", "design", "resilience", "stressors"]
---

# Adapt Design

Change a design so that it survives events that it is not made for.

## Terms

- **Stressor:** an event that the design is not made for.
- **Naive design:** the design before adaptation. Keep it unchanged. It is the control for evaluation.
- **Remaining part:** the part of the design that continues to operate after a stressor.
- **Survive:** after the stressor, the remaining part keeps the essential functions, or returns to them with acceptable effort.

## Input

- The design.
- A list of stressors (skill `generate-stressors`).
- Optional: coupling groups and boundary candidates (skill `find-hidden-coupling`).

Do not use stressors that are marked "test". They are for evaluation only.

## Procedure

1. **Keep the naive design.** Make a copy. Do not change it.
2. **Identify the essential functions.** Get them from the design or from the user. Write them as a short list. Survival depends on this list. If it is not clear, ask.
3. **Order the stressors.** If coupling groups are available, take the stressors group by group. Else use the order of the list.
4. **For each stressor:**
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
   6. Do not skip a stressor because it is unlikely or absurd. Its change often helps with real events.
5. **Consolidate.** Merge the changes into one design:
   - Merge changes that do the same thing.
   - Put elements that the same stressors affect inside one boundary, or let them share structure.
   - Separate elements that different stressors affect.
   - Remove links that no function needs.
   - Remove two-way dependencies where possible.
6. **Check again.** Apply all training stressors to the consolidated design. Record which stressors still fail. Repeat steps 4 to 6 until new stressors need little or no new change. Stop after three passes, or when the user says to stop.
7. **Review trade-offs.** List changes that can conflict with what stakeholders want: cost, speed, user experience, organisation. Do not decide these. Give them to the user.
8. **Review failure modes.** For each element that many stressors affect or many changes use, list its technical failure modes. A focus on external events can hide internal failures.

## Rules

- Prefer one change that deals with many stressors to many specific changes.
- Prefer non-technical changes when they are simpler.
- Each change gives the stressor IDs that it deals with.
- Do not use probability to decide.
- Do not use the test stressors.

## Output

1. **Essential functions.**
2. **Stressor results.**

   | ID | Effect on design | Remaining part | Survives | Change |
   |---|---|---|---|---|
   | S01 | Fees triple. Margin becomes negative. | checkout, orders | no | C03 |
   | S04 | Region outage. | none | yes | C03 (reuse) |

3. **Changes.** ID, description, type, elements, stressor IDs.
4. **Adapted design.** Elements, flows, boundaries. Mark what is new or changed.
5. **Naive design.** Unchanged copy, or a reference to it.
6. **Open decisions.** Trade-offs for the user.
7. **Failure modes.** For shared elements.
8. **Remaining failures.** Training stressors that the adapted design does not survive.

## Related skills

- `generate-stressors`: produces the stressors.
- `find-hidden-coupling`: produces the groups.
- `evaluate-design`: measures the result with the test stressors.
