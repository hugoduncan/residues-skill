---
name: generate-stressors
description: >
  Generate a broad, random list of stressors for a given design or architecture.
  A stressor is an event that the design is not made for. Use when the user asks
  to generate stressors, stress a design, find what can break an architecture,
  list unexpected events for a system, or prepare input for an impact or coupling
  analysis. Triggers: "stressors", "stress the design", "what could hit this
  system", "unknown events", "residual analysis input".
license: EPL-2.0
lambda: "λdesign. scope ∧ unique(elements(design)) → generate(categories × techniques, ¬probability, include(absurd)) → stressors{id category event affects set} → split? → coverage → run_record"
metadata:
  tags: "architecture, design, resilience, stressors"
---

# Generate Stressors

Generate many stressors for a design. Use them to find weak and hidden connections in the design.

## Stressor

A stressor is an event in the future of a system. The design is not made for this event.

- Most stressors come from the environment of the system: business, people, law, money, suppliers, customers, the physical world. Some come from the technology.
- Probability is not relevant. Do not filter stressors by probability or by impact.
- Absurd and impossible events are valid. They often touch the same parts of the design as real events that nobody predicted.
- A stressor is not a requirement, not a risk score and not a mitigation.

## Input

A design or architecture: a document, a diagram description, code, or a conversation.

If the design is not clear, ask for it. Do not invent the design.

## Run record

Write the results to a run record: a directory that the user chooses, for example `stressor-runs/<run-id>/`. Other skills read it. Start each file with the line `# run: <run-id> | date: <date> | skill: generate-stressors`.

| File | Content |
|---|---|
| `design.md` | The design, or a reference to it. Scope and level of detail. |
| `elements.tsv` | Columns: `id`, `name`, `kind`, `description`. |
| `stressors.tsv` | Columns: `id`, `category`, `stressor`, `affects`, `set`. `affects` is a comma-separated list of element IDs. |

Do not change files that other skills wrote. If there is no file access, output each file as a fenced block under its file name. The user saves them.

## Procedure

1. **Extract the elements.** List the elements of the design that a stressor can touch: actors, components, information flows, data stores, infrastructure, external dependencies, business context.
   - If the design is too large to read completely, agree a scope or a coarse level of detail with the user. Record it in `design.md`.
   - Give each element a unique ID. If two elements have the same name, add a qualifier, for example `service (billing)`. Do not merge elements only because their names are the same.
2. **Generate.** Read [references/prompts.md](references/prompts.md). Combine each category with different techniques. Do not select only the combinations that seem likely. Move through the combinations in a fixed or random order.
3. **Write each stressor** with the rules in "Stressor quality".
4. **Map.** For each stressor, list the IDs of the elements that it affects. If it affects no element, write `none`. Do not describe how the design responds.
5. **Remove duplicates.** Merge two stressors only if they are the same event. Keep different events that affect the same elements. That overlap is useful.
6. **Report coverage.** Count stressors for each category. Identify categories with few stressors and elements with no stressors. Generate more stressors for these gaps.
7. **Split, only if the user plans to change or evaluate the design.** Mark 25% of the stressors `test` (or the share the user gives, 20% to 30%). Mark the rest `training`. Each stressor is in exactly one set. Select at random: use code with a seed if possible, else take every fourth stressor in ID order. Record the method and the date in the first line of `stressors.tsv`. Do not change the split later. If the user does not plan this, leave `set` empty.

Default quantity: 60 stressors. Use the quantity that the user gives, if any. Use at least 8 categories. Make at least 10% absurd.

## Stressor quality

- Write one event per stressor.
- Make it concrete: who or what changes, and how.
- Write the event, not the effect on the system. Correct: "The payment provider triples its fees." Incorrect: "Payments become expensive."
- Do not include probability, impact scores or mitigations.

## Output

The run record files, and this table and coverage summary for the user:

| id | category | stressor | affects | set |
|---|---|---|---|---|
| S01 | Suppliers and partners | The payment provider triples its fees. | payment-svc, pricing, checkout-flow | training |
| S02 | Law and regulation | A new law requires that all customer data stays in the country of the customer. | customer-db, analytics-flow, cloud-region | test |
| S03 | Absurd | All customers change their names to the same name on the same day. | customer-db, identity-svc, support-staff | training |

Coverage summary: stressors for each category, elements with no stressors, elements that many stressors affect.

Add other columns only if the user asks.

## Related skills

- `find-hidden-coupling`: uses `affects` to find coupled elements.
- `adapt-design`: changes the design so that it survives the training stressors.
- `evaluate-design`: uses the test stressors to compare the original and the changed design.
