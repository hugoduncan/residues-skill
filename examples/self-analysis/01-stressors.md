# Step 1: generate-stressors

Design: [00-design.md](00-design.md). Full table: [stressors.tsv](stressors.tsv) (ID, category, stressor, affects).

60 stressors. 13 categories. 8 absurd (13%).

Split: 45 training, 15 test. Random, seed 42, done before adaptation ([analyse.py](analyse.py) `split` → [split.tsv](split.tsv)).

## Coverage

| Category | Stressors | Of which test |
|---|---|---|
| Market | 4 | 1 |
| Customers and users | 8 | 4 |
| Organisation and people | 4 | 2 |
| Law and regulation | 4 | 1 |
| Money | 4 | 0 |
| Suppliers and partners | 5 | 0 |
| Technology | 5 | 0 |
| Data | 6 | 2 |
| Security | 4 | 2 |
| Physical world | 2 | 0 |
| Society and politics | 2 | 1 |
| Time | 4 | 1 |
| Absurd | 8 | 1 |

- Elements with no stressors: none.
- Elements with few stressors: `limits` (3), `desc`, `gen-tables`, `decisions`, `code-tool` (5 each).
- Elements that many stressors affect: `ed` (22), `ad` (18), `gs` (16), `fhc` (16), `stressors` (14).
- Gaps: Physical world and Society and politics have only 2 stressors each. For a skill pipeline, these categories mostly affect the model and the harness.

## Examples

| ID | Category | Stressor | Affects |
|---|---|---|---|
| S14 | Organisation and people | A team of five shares the work. Each person runs a different step. | user, test-mark, naive, stressors, decisions |
| S30 | Technology | Each skill runs in a new session. No context passes between steps. | context, stressors, naive, groups, test-mark, essentials |
| S53 | Absurd | Every design element has the name "service". | elements, affects, fhc, groups |
