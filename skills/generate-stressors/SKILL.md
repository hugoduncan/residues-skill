---
name: generate-stressors
description: >
  Generate a broad, random list of stressors for a given design or architecture.
  A stressor is an event that the design is not made for. Use when the user asks
  to generate stressors, stress a design, find what can break an architecture,
  list unexpected events for a system, or prepare input for an impact or coupling
  analysis. Triggers: "stressors", "stress the design", "what could hit this
  system", "unknown events", "residual analysis input".
lambda: "λdesign. elements(design) → generate(categories × techniques, ¬probability, include(absurd)) → stressors{id category event affects} → coverage"
metadata:
  tags: ["architecture", "design", "resilience", "stressors"]
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

## Procedure

1. **Extract the elements.** List the elements of the design that a stressor can touch. Use the names from the design.
   - actors: users, customers, staff, partners
   - components and services
   - information flows: data from one actor or component to a different one
   - data stores
   - infrastructure and platforms
   - external dependencies: suppliers, third-party services, standards
   - business context: revenue, contracts, regulation, market
2. **Generate.** Combine each category with different techniques (see tables). Do not select only the combinations that seem likely. Move through the combinations in a fixed or random order.
3. **Write each stressor** with the rules in "Stressor quality".
4. **Map.** For each stressor, list the elements that it affects. Use the element names from step 1. If a stressor affects no element, keep it and write "none". Do not describe how the design responds.
5. **Remove duplicates.** Merge two stressors only if they are the same event. Keep different events that affect the same elements. That overlap is useful.
6. **Report coverage.** Count stressors for each category. Identify categories with few stressors and elements with no stressors. Generate more stressors for these gaps.

Default quantity: 60 stressors. Use the quantity that the user gives, if any. Use at least 8 categories. Make at least 10% absurd.

## Categories

| Category | Examples of sources |
|---|---|
| Market | competitors, demand, new products, market collapse |
| Customers and users | behavior, volume, expectations, abuse, a new type of user |
| Organisation and people | key staff, reorganisation, merger, strike, skills |
| Law and regulation | new law, audit, data residency, licence, court decision |
| Money | cost, price, currency, funding, payment method |
| Suppliers and partners | supplier failure, contract change, acquisition, price change |
| Technology | platform end of life, outage, vendor lock, library change |
| Data | wrong data, lost data, new data source, schema change, volume |
| Security | attack, leaked credentials, insider, fraud |
| Physical world | weather, fire, pandemic, power, geography |
| Society and politics | sanctions, war, public opinion, media |
| Time | deadlines, time zones, slow change over years, sudden change |
| Absurd | impossible or ridiculous events |

## Techniques

| Technique | Prompt |
|---|---|
| Remove | An actor, supplier, flow, store or component is removed. |
| Scale | A quantity becomes 0, 10 times, or 1000 times larger. |
| Reverse | A flow or relationship goes in the opposite direction. A partner becomes a competitor. |
| Change the rules | A law, contract, policy or price changes. |
| Replace | A different actor, technology or supplier takes the place of the current one. |
| Corrupt | Data, a message or a person gives wrong information. |
| Delay | An event or flow is late by seconds, days or years. |
| Combine | Two unrelated stressors occur at the same time. |
| Absurd | Something impossible happens. Make it concrete. |

## Stressor quality

- Write one event per stressor.
- Make it concrete: who or what changes, and how.
- Write the event, not the effect on the system. Correct: "The payment provider triples its fees." Incorrect: "Payments become expensive."
- Do not include probability, impact scores or mitigations.
- Use short sentences.

## Output

A markdown table, then a coverage summary.

| ID | Category | Stressor | Affects |
|---|---|---|---|
| S01 | Suppliers and partners | The payment provider triples its fees. | payment service, pricing, checkout flow |
| S02 | Law and regulation | A new law requires that all customer data stays in the country of the customer. | customer store, analytics flow, cloud region |
| S03 | Absurd | All customers change their names to the same name on the same day. | customer store, identity service, support staff |

Coverage summary:

- number of stressors for each category
- elements with no stressors
- elements that many stressors affect

Add columns or sections only if the user asks. For example, if the user asks for a test set, mark a random 20% to 30% of the stressors as "test". Do not use the test set to change the design.

## Related skills

- `find-hidden-coupling`: uses the stressors and the "Affects" column to find coupled elements.
- `adapt-design`: changes the design so that it survives the stressors.
- `evaluate-design`: uses test stressors to compare the original and the changed design.
