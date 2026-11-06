---
name: evaluate-design
description: >
  Measure if an adapted design survives unknown events better than the original
  design. Apply a set of test stressors, not used during design, to both designs
  and calculate the index Ri = (R - N) / S. Use when the user asks if a design
  change made a system more resilient, to compare two architectures under stress,
  or to verify adapt-design results. Triggers: "evaluate the design", "compare
  architectures", "residual index", "Ri", "did it get better", "test set".
lambda: "λ(naive, adapted, test_stressors). fix(survival_criteria) → ∀s: survives?(naive, s) ∧ survives?(adapted, s) → N, R, S → Ri = (R − N) / S ∧ regressions"
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
- **Survive:** after the stressor, the design keeps the essential functions, or returns to them with acceptable effort.

## Input

- The naive design.
- The adapted design.
- Test stressors.
- The essential functions.

If there are no test stressors, generate them with skill `generate-stressors`. Use the naive design only as input. Do not look at the adapted design or at the changes. Stressors that you write with knowledge of the changes make the result too good.

If the essential functions are missing, get them from the user before the evaluation.

## Procedure

1. **Fix the criteria.** Write the essential functions and the meaning of "acceptable effort". Do not change them during the evaluation.
2. **Evaluate each test stressor.**
   1. Apply it to the naive design. Follow the flows. Decide: survives or not. Write one reason.
   2. Apply it to the adapted design in the same way. Decide and write one reason.
   3. If neither design survives, decide which design survives better: less loss of essential function, or a faster return. Mark that design as the better one. If they are equal, mark neither.
   Use the same strictness for both designs. Do not give credit for a change that the adapted design does not contain.
3. **Count.**
   - S = number of test stressors
   - N = number of stressors that the naive design survives, plus the number where neither survives and the naive design is better
   - R = number of stressors that the adapted design survives, plus the number where neither survives and the adapted design is better
4. **Calculate.**

   ```
   Ri = (R - N) / S        -1 ≤ Ri ≤ 1
   ```

   - Ri > 0: the adapted design survives unknown events better.
   - Ri = 0: no difference.
   - Ri < 0: the adapted design is worse.
5. **Find regressions.** List the stressors that the naive design survives and the adapted design does not. These show costs of the changes.
6. **Optional: repeat.** If the user asks, repeat with different splits of the stressors into training and test sets. Report the range of Ri.

## Rules

- Do not change either design during the evaluation.
- Do not add a stressor to the test set after you see a result.
- If you are not sure about a decision, mark it "uncertain" and give the reason. Count it as your best decision. Report the number of uncertain decisions.
- One evaluation is not proof. A small test set gives a coarse result.

## Output

1. **Criteria.** Essential functions. Meaning of acceptable effort.
2. **Results.**

   | ID | Stressor | Naive | Adapted | Better if neither | Note |
   |---|---|---|---|---|---|
   | T01 | The cloud provider closes the region. | no | yes | | C03 gives a second region |
   | T02 | A key supplier goes bankrupt. | no | no | adapted | manual fallback C07 |

3. **Counts.** S, N, R.
4. **Ri.** Value and interpretation.
5. **Regressions.**
6. **Uncertain decisions.** Number and IDs.
7. **Next steps.** Stressors that both designs fail. Use them as input for a new adaptation pass. After you use them, they are not test stressors.

## Related skills

- `generate-stressors`: produces the test stressors.
- `adapt-design`: produces the adapted design.
