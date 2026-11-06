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
lambda: "λ(stressors, design). matrix(stressor × element) → {vulnerable(elements) dangerous(stressors) similar(element_pairs) ∖ connected(design)} → groups → boundary_candidates"
metadata:
  tags: ["architecture", "design", "coupling", "resilience", "stressors"]
---

# Find Hidden Coupling

Find the parts of a design that are connected through the events that affect them.

## Idea

If one event affects two elements, the two elements are coupled. The design can show no connection between them. This is hidden coupling. It becomes visible only when the event occurs. This skill makes it visible before the event.

A stressor is an event that the design is not made for.

## Input

- A list of stressors. For each stressor, the elements that it affects.
- The design: elements and the connections between them.

If the stressors are missing, generate them first (skill `generate-stressors`). If the affected elements are missing, map each stressor to the elements first. Do not describe how the design responds.

## Procedure

1. **Normalise the elements.** Use one name for each element. Merge synonyms. If an element is vague, for example "backend" or "the system", split it into the elements of the design. If the design does not give the split, ask. Vague elements hide coupling.
2. **Build the incidence matrix.** Rows are stressors. Columns are elements. Mark a cell if the stressor affects the element.
3. **Find vulnerable elements.** Count the marks in each column. The elements with the most marks are the most vulnerable.
4. **Find dangerous stressors.** Count the marks in each row. The stressors with the most marks are the most dangerous. They spread through the most of the design.
5. **Compare elements.** For each pair of elements A and B:
   - shared = number of stressors that affect A and B
   - union = number of stressors that affect A or B
   - similarity = shared / union
   - A pair is coupled if similarity ≥ 0.5 and shared ≥ 3. Use different limits if the user gives them, or if the list has fewer than 20 stressors.
6. **Find hidden coupling.** For each coupled pair, check the design. If the design shows no direct connection between A and B, the coupling is hidden. If the design shows a connection, the coupling is known.
7. **Build groups.** Connect the coupled pairs. Each connected set of elements is a group.
8. **Check dependencies.** Build a dependency matrix from the design: rows and columns are elements, a mark shows that the row element uses the column element. Identify:
   - two-way dependencies (A uses B and B uses A). Failure can spread in both directions.
   - links that no stressor pattern supports and no function needs. These are candidates for removal.
9. **Identify boundary candidates.**
   - Elements in the same group: candidates to put inside one boundary, or to share structure.
   - Elements with a unique pattern: candidates for a separate boundary, for example a separate service.
   - Hidden coupling across an existing boundary: candidate for a boundary change.
   Give the stressor IDs that support each candidate. Do not design the change. That is a different task.

For more than 30 stressors or more than 15 elements, calculate the counts and similarities with code if a tool is available. Do not calculate large matrices by hand.

## Rules

- Use only the stressors and the design. Do not add stressors during the analysis. Record gaps instead.
- Do not filter by probability.
- Do not use stressors that the user marks as "test".
- Report the limits that you used.

## Output

1. **Incidence matrix.** Use a table. For many stressors, show only the stressors that affect two or more elements, and give the full matrix in a file if possible.
2. **Vulnerable elements.** Element, number of stressors, stressor IDs.
3. **Dangerous stressors.** Stressor ID, stressor, number of elements.
4. **Coupled pairs.**

   | A | B | Shared | Similarity | In design | Stressors |
   |---|---|---|---|---|---|
   | payment service | customer store | 4 | 0.67 | no (hidden) | S01, S07, S12, S30 |

5. **Groups.** Elements in each group, and the stressors that the group shares.
6. **Dependency findings.** Two-way dependencies. Unsupported links.
7. **Boundary candidates.** Candidate, elements, supporting stressors.
8. **Gaps.** Elements that no stressor affects. Vague elements that the user must split.

## Related skills

- `generate-stressors`: produces the input.
- `adapt-design`: uses the groups to change the design.
