---
name: evaluate-design
description: >
  Measure if an adapted design survives unknown events better than the original
  design. Apply a set of test stressors, not used during design, to both designs
  and calculate the index Ri = (R - N) / S. Use when the user asks if a design
  change made a system more resilient, to compare two architectures under stress,
  or to verify adapt-design results. Triggers: "evaluate the design", "compare
  architectures", "residual index", "Ri", "did it get better", "test set".
lambda: "λ(naive, adapted, test_stressors). check(inputs ∧ disjoint(split) ∧ provenance) ∧ use(criteria) → ∀s: survives?(naive, s) ∧ survives?(adapted, s) → N, R, S → check(counts) → Ri = (R − N) / S ∧ regressions"
metadata:
  tags: ["architecture", "design", "resilience", "evaluation", "stressors"]
---

# Evaluate Design

Measure if a changed design survives unknown events better than the original design.

## Terms

- **Stressor:** an event that the design is not made for.
- **Naive design:** the original design. It is the control.
- **Adapted design:** the changed design.
- **Test stressors:** stressors that nobody used to change the design. For the design, they are unknown events.
- **Criteria:** the essential functions, and the meaning of "acceptable effort".
- **Survive:** after the stressor, the design keeps the essential functions, or returns to them with acceptable effort.

## Input

- The naive design.
- The adapted design.
- Test stressors.
- The criteria.

## Run record

If the user gives a run record directory, read and write files there. Start each file that you write with `# run: <run-id> | date: <date> | skill: evaluate-design`. If there is no file access, output each file as a fenced block under its file name.

| File | Use |
|---|---|
| `naive.md`, `adapted.md`, `stressors.tsv`, `criteria.md`, `adaptation.md` | read |
| `evaluation.md` | write |

## Procedure

1. **Check the inputs.** If the naive design or the adapted design is missing, stop and ask. Do not derive the naive design from the adapted design. Do not use one design for both.
2. **Check the test set.**
   - Each stressor is in exactly one set. If a stressor is in both sets, or the test set is empty, stop and report.
   - Find the provenance. Compare the date of the split (first line of `stressors.tsv`) with the start of the adaptation (`naive.md`, `adaptation.md`). Report: split recorded before adaptation: yes, no or unknown.
   - If there are no test stressors, generate them with skill `generate-stressors`. Use only the naive design as input. Do not look at the adapted design or at the changes. Report the provenance: generated at evaluation.
3. **Use the criteria.** Use `criteria.md` unchanged. If it is missing, get the criteria from the user, write `criteria.md`, and report that the criteria of the adaptation are unknown. Do not change the criteria during the evaluation.
4. **Evaluate each test stressor.**
   1. Apply it to the naive design. Follow the flows. Decide: survives or not. Write one reason.
   2. Apply it to the adapted design in the same way. Decide and write one reason.
   3. If neither design survives, decide which design survives better: less loss of essential function, or a faster return. Mark that design as the better one. If they are equal, mark neither.
   Use the same strictness for both designs. Do not give credit for a change that the adapted design does not contain.
5. **Count.**
   - S = number of test stressors
   - N = number that the naive design survives, plus the number where neither survives and the naive design is better
   - R = number that the adapted design survives, plus the number where neither survives and the adapted design is better
6. **Check the counts.** Each stressor counts at most once for each design. N ≤ S. R ≤ S. Use code if possible. If a check fails, count again.
7. **Calculate.**

   ```
   Ri = (R - N) / S        -1 ≤ Ri ≤ 1
   ```

   - Ri > 0: the adapted design survives unknown events better.
   - Ri = 0: no difference.
   - Ri < 0: the adapted design is worse.
8. **Find regressions.** List the stressors that the naive design survives and the adapted design does not.
9. **Optional: repeat.** If the user asks, repeat with different splits. Report the range of Ri.

## Rules

- Do not change either design during the evaluation.
- Do not add a stressor to the test set after you see a result.
- If possible, evaluate in a new session, or let a different person evaluate. The author of the changes is biased.
- If you are not sure about a decision, mark it "uncertain" and give the reason. Count it as your best decision. Report the number of uncertain decisions.
- One evaluation is not proof. A small test set gives a coarse result.

## Output

`evaluation.md`:

1. Inputs and provenance of the test set.
2. Criteria.
3. Results:

   | ID | Stressor | Naive | Adapted | Better if neither | Note |
   |---|---|---|---|---|---|
   | T01 | The cloud provider closes the region. | no | yes | | C03 gives a second region |
   | T02 | A key supplier goes bankrupt. | no | no | adapted | manual fallback C07 |

4. Counts: S, N, R. Result of the count checks.
5. Ri, and its interpretation.
6. Regressions.
7. Uncertain decisions: number and IDs.
8. Next steps: stressors that both designs fail. Use them in a new adaptation pass. After that use, they are not test stressors.

## Related skills

- `generate-stressors`: produces the test stressors.
- `adapt-design`: produces the adapted design.
