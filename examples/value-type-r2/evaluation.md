# run: value-type-r2 | date: 2026-11-06 | skill: evaluate-design

# Evaluation: value-type (r2)

Evaluator: independent session. This session did not write the stressors, the adaptation or the adapted design.

## 1. Inputs and provenance

- Naive design: `naive.md` (value-type commit `5073893f`). Source files read with `git show 5073893f:<path>`: `src/value_type/core.clj`, `capability.clj`, `impl/{capability,loader,runtime,class_file,field_access,transform}.clj`, `impl/identity_backend.clj` (part), `deps.edn`, `bb.edn`, `.github/workflows/ci.yml`, `README.md` (part), `ramora/defvaluetype-design/risks-and-evolution.md`.
- Adapted design: `adapted.md`, with changes C01–C11 of `adaptation.md`.
- Criteria: `criteria.md`. Status CONFIRMED. Used unchanged.
- Test set: `stressors.tsv`, `set` = `test`. 31 stressors. 93 training stressors. No stressor is in both sets. No duplicate IDs.
- Split recorded before adaptation: **yes**.
  - The split line has the date 2026-11-06 and says "before adaptation".
  - Git: `stressors.tsv` and `naive.md` are in commit `bd5b39f` (19:09:56 −0500). `adaptation.md` and `adapted.md` are in the later commit `e94b9ac` (19:16:24 −0500). `stressors.tsv` did not change after that.
  - No test stressor ID occurs in `adaptation.md` or `adapted.md`.
- Bias: the same agent wrote the stressors and the adaptation (`adaptation.md` says this).

## 2. Criteria

From `criteria.md`, unchanged:

- F1 definition (value class, or identity class as the policy permits). F2 policy controls the representation. F3 `:non-nil` checks. F4 public namespaces load on baseline JVMs. F5 native arrays or a clear failure. F6 true capability report. F7 consumers can get the library; the maintainer can verify it on the claimed JVMs.
- Survive: F1–F7 hold, or return with acceptable effort. A clear, early failure that names the cause and the fix keeps the function in an unsupported environment. Silent wrong behaviour does not survive. Loss of value output on a JVM that is not claimed is acceptable.
- Acceptable effort: the maintainer alone, a few days, one boundary (at most two namespaces plus test rows, or documentation or configuration only), no public syntax change, no new supplier, JVM agent or Java source.

## 3. Results

| ID | Stressor | Naive | Adapted | Better if neither | Note |
|---|---|---|---|---|---|
| S004 | Users increase from 10 to 100000 in one month. | yes | yes | | More support work. Install from the repository (naive) or Clojars (C04) works. No function changes. |
| S006 | Clojure contrib publishes an alternative. | yes | yes | | Adoption only. No function changes. |
| S007 | closed-record users report all defects against value-type. | yes | yes | | Maintainer load only. |
| S019 | AI agents open 500 pull requests in one week. | yes | yes | | Nothing merges without the maintainer. The maintainer can close or limit pull requests (configuration). |
| S020 | A contributor rewrites the value backend in Java. | yes | yes | | The maintainer can refuse the change. The design stays Clojure only. |
| S022 | The Valhalla team hires the maintainer and forbids public work. | yes | yes | | Code, tests and repository stay public. No function stops at the event. Uncertain: no maintainer for later changes. |
| S025 | The closed-record maintainer leaves. | yes | yes | | value-type tests the record and closed shapes itself. No dependency on closed-record. |
| S029 | Export control classifies preview features as dual-use. | yes | yes | | Where preview is not available: fallback by policy (F1, F2). CI download is not in scope of the restriction. |
| S030 | AI-written code has no copyright. | yes | yes | | Licence text needs a documentation change. Code stays available. |
| S045 | Clojure 1.13 replaces NewInstanceExpr. | yes | yes | | Naive: transform gives `:unexpected-constructor`, identity backend `:unsupported-shape`, both with "Fix: use Clojure 1.12". Clojure 1.13 is not supported, so a clear failure keeps F1. Adapted: C01 compiler check gives `:unsupported-compiler`, then fallback by policy; fix in one boundary. Uncertain: if the new compiler does not define through `Compiler/LOADER`, the naive identity path with `:non-nil` fields loses its checks silently. |
| S046 | Clojure removes the class cache of DynamicClassLoader. | yes | yes | | Naive: the capture proxy defines in a delegate and finds the class through the static cache, so capture fails with class-not-found errors. Fix in `impl.loader` only. Adapted: C01 detects it and falls back by policy; fix in the compiler boundary. |
| S048 | Adoptium Valhalla builds use different flags. | yes | yes | | Build not claimed. Naive: probe failure or `:unsupported-class-version`; flags are in two namespaces (`impl.capability`, `transform`), so support is acceptable effort. Adapted: C09 lookup miss gives fallback; add one row. |
| S054 | Clojure compiles protocol calls to invokedynamic. | yes | yes | | Transforms change only constructors and field instructions. Other instructions pass through. |
| S059 | A new EA GC moves flattened fields; Unsafe offsets fail. | yes | yes | | value-type uses no Unsafe. The new build is not claimed. |
| S065 | Editor hot-swap; report shows the result from before the swap. | yes | yes | | Capability is a property of the running JVM. A class swap does not change it. The cached result stays true (F6). |
| S073 | A false `value-type.impl` namespace is earlier on the class path. | no | no | | Neither design detects namespace shadowing. All functions fail silently. C08 signs only the real JAR. Uncertain: the cause is in the application dependencies. |
| S075 | Secrets of value objects appear in heap dumps of flat arrays. | yes | yes | | Not an essential function. Identity objects have the same exposure. |
| S084 | A war blocks the maintainer's access to GitHub and Oracle sites. | yes | yes | | Consumers still get the code. Naive: local tests use a local Valhalla JDK (`JAVA_CMD`), so the maintainer can verify. Adapted: also C07 archive, C04 mirror, C08 key outside GitHub. Uncertain: naive has no guaranteed JDK copy. |
| S086 | The Clojure community splits into two forks. | yes | yes | | At the split, both forks have the same compiler output. Later divergence is as S045. Uncertain: long-term cost of two compiler lines. |
| S092 | JEP 401 becomes final, two years early. | yes | yes | | Final JDK is not claimed. Naive: without `--enable-preview`, `:unsupported-class-version` and fallback; the version rule is in two namespaces, so the change is acceptable effort. Adapted: C09 lookup miss gives fallback; add one row. Uncertain: the field probe throws "accepted null" if the final JVM ignores `NullRestricted` (both designs). |
| S094 | A server runs five years; JVM files change below it. | yes | yes | | Cached capability stays true for the running JVM. File replacement is a general JVM risk. |
| S099 | Every value object is `==` to nil. | no | no | | `nil?` is true for every value object, silently (F1). Naive probe does not compare with nil. C11 compares two objects with each other, not with nil. |
| S103 | Each JVM start uses a random class-file major version. | yes | yes | | Naive: probe and transform read the latest major version at run time; value AOT output fails clearly (documented). Adapted: C09 lookup miss gives fallback by policy on an absurd, not-claimed JVM. Adapted loses more value output, but survives. |
| S107 | Every user believes that fallback classes are value classes. | yes | yes | | The library behaves as specified. Docs, policy `warn`/`error` and the report show the representation. |
| S108 | Constructors run after the methods of the object. | no | no | | JVM semantics fail. Clojure `deftype` also fails. No library change can help. |
| S109 | GitHub deletes every repository with 'value' in its name. | yes | yes | | Naive: the maintainer pushes the local clone to a new name or host; documentation change. Adapted: also Clojars and mirror (C04). |
| S115 | Operators disable `java.lang.classfile` with a JVM flag. | yes | yes | | If the class is not found: `:missing-classfile-api`, fallback by policy. If calls throw: the error propagates; the fix is in one namespace. Same flow in both. |
| S116 | A build tool evaluates cached expansions on a different JDK. | yes | yes | | Receiving forms check capability again (`:value-capability-unavailable`). Ordinary value expansions fail with `:not-value-class` and name the fix. Fallback expansions apply the receiver policy. |
| S117 | nREPL middleware sends macroexpanded forms to a remote JVM. | yes | yes | | Same flows as S116. Uncertain: a local JVM without value classes gives a guarded identity form; a capable remote JVM with `silent` accepts it with no message (documented behaviour). |
| S121 | Monitoring calls `capability/report` on each request. | yes | yes | | Results are cached. The report does not change, so no alerts. Low cost. |
| S122 | clojure.asm and java.lang.classfile write the same bytes for every class. | yes | yes | | Read as: both writers give equal output. No effect. Uncertain: if read as "one constant byte array for all classes", Clojure stops and neither design survives. |

## 4. Counts

- S = 31
- N = 28
- R = 28

Checks (Python, run in this session): each test ID counts at most once for each design; "better if neither" is empty where a design survives; N ≤ S; R ≤ S; test and training sets are disjoint. All checks pass.

## 5. Ri

```
Ri = (R − N) / S = (28 − 28) / 31 = 0.00
limits: max (S − N) / S = 3/31 = 0.097, min −N / S = −28/31 = −0.903
```

- Ri = 0: no measured difference between the designs on this test set.
- S − N = 3 < 5. Ri cannot show an effect with this test set. The naive design already survives 28 of 31 stressors. The three stressors that remain are absurd or outside the library boundary.
- Recommendation: get more test stressors that stress the naive design (compiler, JVM format, release), or repeat with different splits (skill step 9). Each split needs its own adaptation.
- Observation (not counted): in S045, S046, S048, S084 and S092 the adapted design gives an earlier fallback or a smaller fix boundary (C01, C07, C09). The binary decision does not show this.

## 6. Regressions

None. No test stressor that the naive design survives fails in the adapted design.

Note: C09 changes an unknown major version or build from value output to fallback (S103). This is a loss of value output on a JVM that is not claimed, so it is not a regression under the criteria.

## 7. Uncertain decisions

8: S022, S045, S073, S084, S086, S092, S117, S122. Reasons are in the table. Each counts as the best decision. No uncertain decision changes R − N, because both designs have the same decision for each one.

## 8. Next steps

Both designs fail S073, S099 and S108. Use them in a new adaptation pass. After that use, they are not test stressors.

- S073: think about a load-time check that the `value-type.impl` namespaces come from the same artifact.
- S099: C11 can also compare a value object with nil.
- S108: absurd. No library change is likely to help.
