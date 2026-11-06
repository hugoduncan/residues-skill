# Step 3: adapt-design — Open decisions and failure modes

Index: [../03-adaptation.md](../03-adaptation.md)

## Open decisions

- D1: Frontmatter. Keep `lambda` and `metadata` (helps S28, project convention), or use only `name` and `description` (helps S25). Recommendation: keep.
- D2: C07 adds a split step. Users who want only a stressor list do not need it. Option: gs splits only when the user plans to adapt. ad asks.
- D3: C04 needs file access. A chat-only harness has none. Fallback: output the record as one markdown block for the user to save.
- D4: C05 adds a script. The skill is then not text only. Language: Python (common) or Babashka (project convention).

## Failure modes of shared elements

- Run record: files from an older run mix with a new run. Put a run ID and a date in each file.
- Criteria record: vague essential functions make every survival decision vague.
- Reference script: a bug gives wrong groups for every run. Test it with a known matrix.
- Model: the same model adapts and evaluates (self-assessment bias). Run ed in a new session or by a different person.

## Remaining failures

S25 (open decision D1).
