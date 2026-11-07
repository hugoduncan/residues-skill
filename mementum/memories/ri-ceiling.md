💡 Ri has a ceiling: Ri ≤ (S − N) / S, and a floor: Ri ≥ −N / S.

When the naive design already survives most test stressors (good existing risk analysis), Ri cannot show an effect, even if the adaptation is real. Ri = 0.00 then does not mean "no improvement".

Example: value-type r1 (examples/value-type). S = 18, N = 16 → ceiling 2/18 = 0.11. Result Ri = 0.00.

Consequences (applied in the skills, 2026-11-06):
- evaluate-design reports the limits. If S − N < 5, it reports that Ri cannot show an effect (threshold is a heuristic, not from the source).
- More stressors give more naive failures and a finer step (1/S). They do not raise the ceiling ratio. Do not filter stressors by impact to raise it.
- Repeated splits give a range of Ri. Each split needs its own adaptation, because an adaptation must not see its test stressors.

Check the ceiling before reading any Ri.
