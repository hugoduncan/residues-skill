---
name: find-hidden-coupling
description: >
  Find hidden coupling in a design from a list of stressors and the design
  elements that each stressor affects. Builds a stressor-by-element matrix and
  identifies vulnerable elements, dangerous stressors, and elements that the same
  events affect. Use after generating stressors, or when the user asks which
  parts of a design are coupled, vulnerable, or should share or split a boundary.
  Triggers: "hidden coupling", "incidence matrix", "which components are coupled",
  "vulnerable components", "dangerous stressors", "where to put boundaries".
license: EPL-2.0
lambda: "λ(stressors, design). normalise(unique(elements)) → script(matrix(stressor × element)) → mapping_check → {vulnerable dangerous similar(pairs) ∖ connected(design)} → (hidden = ∅ → sensitivity(lower similarity)) → groups → boundary_candidates"
metadata:
  tags: "architecture, design, coupling, resilience, stressors"
---

# Find Hidden Coupling

Find the parts of a design that are connected through the events that affect them.

## Idea

If one event affects two elements, the two elements are coupled. The design can show no connection between them. This is hidden coupling. It becomes visible only when the event occurs. This skill makes it visible before the event.

A stressor is an event that the design is not made for.

## Input

- Stressors. For each stressor, the IDs of the elements that it affects.
- The design: elements and the connections between them.

If the stressors are missing, generate them first (skill `generate-stressors`). If the affected elements are missing, map each stressor to the elements first. Do not describe how the design responds.

## Run record

If the user gives a run record directory, read and write files there. Start each file that you write with `# run: <run-id> | date: <date> | skill: find-hidden-coupling`. If there is no file access, output each file as a fenced block under its file name.

| File | Use |
|---|---|
| `design.md` | read |
| `elements.tsv` | read. Update only in step 1. |
| `stressors.tsv` | read. Update only the `affects` column in step 1. |
| `connections.tsv` | write. Columns: `from`, `to`. One row for each "from uses to". |
| `coupling.md` | write. The output. |

Without a run record, use the same file formats in a temporary directory.

## Procedure

1. **Normalise the elements.**
   - Use one unique ID for each element. Merge two elements only if they are the same element, not only because the names are the same.
   - If an element is vague, for example "backend" or "the system", split it into the elements of the design. If the design does not give the split, ask. Vague elements hide coupling.
   - If the design is too large to read completely, agree a scope or a coarse level with the user.
   - Record each change to elements or to `affects` in `coupling.md`.
2. **Write the connections.** From the design, write `connections.tsv`.
3. **Run the counts.** Run `python3 scripts/coupling.py <run-dir>` from this skill directory. Options: `--min-similarity` (default 0.5), `--min-shared` (default 3), `--force`. Use smaller limits if the user gives them, or if there are fewer than 20 stressors. The script ignores `test` rows.
   - If the default limits find no hidden pairs, run again with `--min-similarity 0.35`, then `0.3`, as a sensitivity check. A well-documented design often has hidden pairs only at lower limits. Report them separately, with their limits.
   - Exit 2: invalid input (duplicate stressor IDs, unknown elements). Correct the input. Run again.
   - Exit 3: the mapping check failed. Go to step 4.
   - Without a code tool: count by hand. Compare only pairs with at least the minimum shared stressors. Count the top three results of each list a second time.
4. **Mapping check.** The mapping is too coarse if one element has more than 80% of the stressors, or if more than half of all pairs are coupled. It is too fine if no pairs are coupled, or if more than 80% of the stressors affect one element or none. If the check fails, report the reasons and go back to step 1 or to the mapping. Do not report groups.
5. **Identify boundary candidates.**
   - Elements in the same group: candidates to put inside one boundary, or to share structure.
   - Elements with a unique pattern: candidates for a separate boundary, for example a separate service.
   - Hidden coupling across an existing boundary: candidate for a boundary change.
   - Two-way dependencies: failure can spread in both directions. Candidates for removal.
   - Links that no stressor pattern supports and no function needs: candidates for removal.
   Give the stressor IDs that support each candidate. Do not design the change.

## Method

The script does these calculations on the training stressors:

- **Incidence matrix:** rows are stressors, columns are elements.
- **Vulnerable elements:** the most marks in a column.
- **Dangerous stressors:** the most marks in a row.
- **Similarity** of elements A and B: shared / union. Shared is the number of stressors that affect A and B. Union is the number that affect A or B. A pair is coupled if similarity ≥ minimum and shared ≥ minimum.
- **Hidden coupling:** a coupled pair with no row in `connections.tsv`.
- **Groups:** connected sets of coupled pairs.
- **Two-way dependencies:** A uses B and B uses A.

## Rules

- Use only the stressors and the design. Do not add stressors. Record gaps.
- Do not filter by probability.
- Do not use `test` stressors.
- Report the limits that you used.

## Output

`coupling.md`:

1. Changes to elements and mapping (step 1).
2. Mapping check result.
3. Vulnerable elements. Dangerous stressors.
4. Coupled pairs, one table for each set of limits:

   | A | B | Shared | Similarity | In design | Stressors |
   |---|---|---|---|---|---|
   | payment-svc | customer-db | 4 | 0.67 | no (hidden) | S01, S07, S12, S30 |

5. Groups. Two-way dependencies.
6. Boundary candidates, with stressor IDs.
7. Gaps: elements with no stressors, vague elements.

## Related skills

- `generate-stressors`: produces the input.
- `adapt-design`: uses the groups to change the design.
