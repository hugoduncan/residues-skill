💡 Ri has a ceiling: Ri ≤ (S − N) / S, and a floor: Ri ≥ −N / S.

When the naive design already survives most test stressors (good existing risk analysis), Ri cannot show an effect, even if the adaptation is real. Ri = 0.00 then does not mean "no improvement".

Examples (value-type, same design): r1 S = 18, N = 16 → ceiling 0.11. r2 (124 stressors) S = 31, N = 28 → ceiling 0.10. Both Ri = 0.00. Naive survival ≈ 90% in both: more stressors did not raise the ceiling.

Consequences (in the skills, 2026-11-06):
- evaluate-design reports the limits. If S − N < 5, it reports that Ri cannot show an effect (heuristic threshold).
- More stressors give more naive failures and a finer step (1/S). They do not raise the ceiling ratio. At 90% naive survival, S − N ≥ 5 needs ~50 test stressors (~200 total). Do not filter stressors by impact to raise it.
- Repeated splits give a range of Ri. Each split needs its own adaptation.

Check the ceiling before reading any Ri.
