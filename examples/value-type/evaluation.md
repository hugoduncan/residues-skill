# run: value-type-r1 | date: 2026-11-06 | skill: evaluate-design

# Evaluation: value-type

## 1. Inputs and provenance

| Input | Source | Check |
|---|---|---|
| Naive design | `naive.md` (value-type commit `5073893f`) | present |
| Adapted design | `adapted.md` (C01–C08, C02 merged into C03) | present, different from naive |
| Test stressors | `stressors.tsv`, `set` = `test` | 18 of 73. 55 training. No ID in two sets. No duplicate IDs. |
| Criteria | `criteria.md` | confirmed 2026-11-06, used unchanged |
| Source design | `git show 5073893f:<path>` (`ramora/defvaluetype-design/*`, `src/value_type/*`, `deps.edn`, `.github/workflows/*`, `README.md`) | read only. The working tree is at a later commit, so it was not used. |

Provenance:
- Split line: `random.Random(20261106).sample, 18/73 test (25%), date 2026-11-06, before adaptation`.
- `naive.md` and `adaptation.md` have the date 2026-11-06. The dates are the same. The split line says "before adaptation". File times agree: `stressors.tsv` 18:04, `naive.md` 18:05, `adaptation.md` 18:43.
- `adaptation.md` says "Test stressors were not read". `adaptation.md` and `adapted.md` do not contain test IDs.
- **Split recorded before adaptation: yes.**

Evaluator: a new session. This session did not write the adapted design.

## 2. Criteria

From `criteria.md`, unchanged:
- F1 definition with `deftype` syntax and behaviour: value class if supported, else identity class as the policy permits.
- F2 policy controls representation. A strict failure is never skipped.
- F3 `:non-nil` rejects nil and wrong types on all supported constructor paths.
- F4 public namespaces load without value-class support or optional JDK APIs.
- F5 native arrays on a supported JVM, else a clear failure.
- F6 true capability report.
- F7 consumers can get the library. The maintainer can verify it on the claimed JVMs.
- Survive: F1–F7 hold, or return with acceptable effort (maintainer alone, a few days, at most two namespaces or docs/config only, no public syntax change, no new supplier). A clear early failure that names cause and fix keeps the function. Silent wrong behaviour does not survive. Loss of value-class output on an unclaimed JVM is acceptable.

## 3. Results

| ID | Stressor | Naive | Adapted | Better if neither | Note |
|---|---|---|---|---|---|
| S01 | Clojure core adds value-class support to deftype. | yes | yes | | Naive: Clojure 1.12.6 is pinned; identity `deftype` output does not change, so capture and transform still work; the design plans to retire. Adapted: same; C01 gives policy fallback if the output changes. Uncertain: the new compiler output is unknown. |
| S02 | A competing library takes most users. | yes | yes | | Adoption only. F1–F7 do not change. |
| S04 | Users ask for ClojureScript and ClojureCLR. | yes | yes | | A feature request. F1–F7 are JVM functions and still hold. Other platforms fail clearly (no namespace). |
| S07 | A popular library calls `locking` on value objects. | yes | yes | | Clear `IdentityException`. Documented risk ("users depend on identity"). Return: start without `--enable-preview`, then identity fallback (config only). No change in adapted. |
| S08 | AOT on Java 8, deploy on Valhalla with policy `error`. | yes | yes | | D13 guard throws plain `Error` where the form is evaluated, also on a capable JVM, with a separate diagnostic. Strict policy is not skipped. Fix: rebuild (documented). C08 does not change the guard. |
| S09 | 100000 `defvaluetype` forms evaluated at run time. | yes | yes | | One delegate loader per form, as `Compiler.eval` does for `deftype`. Capability and warning flag are cached. C01 probe runs once. |
| S11 | Java teams load AOT value types with `Class.forName`, no Clojure source. | yes | yes | | Value AOT classes need no source and keep constructor checks (source-free AOT is verified). Other JDK release: clear `UnsupportedClassVersionError`. Uncertain: fallback AOT classes loaded directly bypass the policy guard (documented limit, same in both). |
| S12 | The only maintainer stops work for one year. | yes | yes | | Code is frozen. Consumers clone from Git. EA3 and baseline stay valid; maintainer has a local EA3. `release.yml` downloads EA3 by URL: if the URL goes, a config change. Adapted: C07 archive and C03 table make return easier. Uncertain: EA3 availability after one year. |
| S14 | A new AI model ignores STE and Ramora rules. | yes | yes | | Docs quality falls. Vale and the maintainer's review catch prose. F1–F7 do not change. |
| S18 | EA licence forbids CI use. | yes | yes | | Only `release.yml` uses EA3 in CI. The maintainer verifies locally and removes EA cells from CI (config only). F7 holds. |
| S20 | Clojars removes all EPL artifacts. | yes | yes | | Not published; README installs from Git. Clojure is on Maven Central. `scry` (own library) and other dev deps move to Git or local deps (config only). |
| S31 | Next EA build renames `ValueClass` methods. | yes | yes | | `impl.array` gives `:missing-array-signature`: clear F5 failure, true report. Unclaimed JVM. Fix in one namespace. Adapted: unknown build gives `:unknown-jvm-format` and policy fallback; also acceptable. |
| S36 | CIDER macroexpands each top-level form on each keystroke. | yes | yes | | Naive: ordinary expansion installs a loader in the tooling frame (documented risk; only the target name is captured; a leaked loader is only a parent). Adapted: C08 defers install to analysis. Uncertain: the naive loader chain can grow per keystroke; the C01 probe runs at expansion and its binding context is not specified. |
| S38 | A JIT defect gives wrong values from flattened arrays. | no | no | | JVM defect. Arrays silently give wrong values; no element detects it. Return by JVM flag after detection. Adapted has no change for arrays. Uncertain: defect is outside the library. |
| S42 | Serialized value objects read on a fallback JVM. | yes | yes | | Serialization is not an essential function. Same class name; failure is clear or deserialization works. Design says fallback has identity semantics. |
| S52 | Sanctions block EA downloads in the maintainer's country. | yes | yes | | Local EA3 copy. GitHub runners download EA3 outside the country. F7 holds. Adapted: C07 archive also helps. |
| S58 | The JVM makes all value objects `==`. | no | no | | JVM defect. Default equality and `identical?` silently give wrong results; the probe does not detect it. Return: start without preview (config). No adapted change. Uncertain: defect is outside the library. |
| S71 | Capability report called one million times per second. | yes | yes | | Report reads four cached delays and selects keys. C01 probe result is also cached. |

## 4. Counts

- S = 18
- N = 16 (16 survive; 0 neither-survives cases where naive is better)
- R = 16 (16 survive; 0 neither-survives cases where adapted is better)
- Checks (Python): the result IDs equal the 18 test IDs; each stressor counts at most once for each design; "better" is set only when neither survives; N ≤ S; R ≤ S. All pass.

## 5. Ri

Ri = (R − N) / S = (16 − 16) / 18 = **0.00**.

No difference. On these 18 test stressors the changes C01–C08 give no measured gain. Most test stressors are adoption, process or JVM-defect events. C01–C08 target compiler drift, JVM-format drift and release security, and no test stressor tests these directly. The test set is small, so the result is coarse.

## 6. Regressions

None.

## 7. Uncertain decisions

6: S01, S11, S12, S36, S38, S58. Reasons are in the Note column.

## 8. Next steps

Both designs fail: S38, S58. Use them in a new adaptation pass. After that use, they are not test stressors. Both are silent JVM defects on the claimed JVM. A possible direction: a documented kill switch (for example, force identity or disable native arrays by property) and a runtime self-check of value semantics in the capability probe.
