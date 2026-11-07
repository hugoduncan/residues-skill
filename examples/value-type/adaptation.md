# run: value-type-r1 | date: 2026-11-06 | skill: adapt-design

# Adaptation: value-type

Inputs: `naive.md`, `criteria.md` (confirmed 2026-11-06), `coupling.md`, 55 training stressors. Test stressors were not read in passes 1 and 2.
Pass 3 (2026-11-06, after `evaluation.md`): S38 and S58, the two test stressors that both designs fail (evaluate-design next steps). They are now used. They are not test stressors after this pass. `stressors.tsv` is not changed (the split stays as recorded). `evaluation.md` is the evaluation of the pass-2 design.
Code facts checked at commit `5073893f`: `impl/capability.clj` (probe uses `clojure.asm`; constants `0x800`, `0xffff0000|major`), `impl/transform.clj` (own `ACC_STRICT_INIT`, `ClassFile/PREVIEW_MINOR_VERSION`), `impl/runtime.clj` (policy read once at load; invalid value throws), `core/check-value-class`, `.github/workflows/release.yml` (Clojars credentials in GitHub secrets; `fetch-depth: 0`), release shallow-clone check, tests on `clojure.test`, 405 mentions of EA3 in 204 maintained files.

Order: coupling groups first (compiler group, then JVM-format group, then release group), then the other stressors in ID order.
"Survives" refers to the design at that point, with the earlier changes. `naive: no` shows that the naive design does not survive.

## 1. Stressor results

### Compiler group (clj-compiler, loader, identity-backend)

| ID | Effect on design | Remaining part | Survives | Change |
|---|---|---|---|---|
| S15 | New maintainer lacks compiler knowledge. The compiler facts are in `context.md`, and `loader` is the only namespace that uses `Compiler/LOADER`. | all | yes | — |
| S26 | Apps can override the pinned Clojure version. On 1.13 the D6 shape check fails in `value-transform` and `identity-backend`. The probe still reports "available", so every value and non-nil definition throws, under all policies. The fix touches more than two namespaces and the record shapes. | baseline JVM, ordinary definitions | naive: no → yes | C01 |
| S28 | `let` pushes a new loader, so the capture has no effect. D9 throws `:not-installed` on each value definition. With C01 the probe reports `:unsupported-compiler` and ordinary definitions use fallback by policy. Non-nil definitions need capture on both backends, so they fail clearly. A fix needs a new capture design (D3). | ordinary definitions (fallback) | no | C01 (partial) |
| S35 | native-image: no run-time class definition. Fallback AOT output and its guard work. The capability report throws an unknown probe error (designed: unknown failures propagate). | AOT identity classes | yes | — |
| S39 | Sibling loader tag: exact Class identity is checked through the delegate. The result is `:field-class-mismatch` or correct resolution. | all | yes | — |
| S45 | No custom loaders: Clojure source loading also stops. AOT value and fallback output load without custom loaders. | AOT path | yes | — |
| S69 | `Compiler.eval` always binds `LOADER`. Separate `macroexpand` then `eval` gives the documented D9 `:not-installed` error. Non-nil receiving expansions work. | all | yes | — |
| S06 | 2000 fields exceed the JVM 255-slot parameter limit. `deftype` fails in the same way. The value path wraps the error as `:jvm-rejected`. | all (same as deftype) | yes | — |
| S27 | `impl.capability` imports `clojure.asm` and `core` loads it eagerly, so the public namespaces fail to load on every JVM (F4, F1 lost). | none | naive: no → yes | C02 |
| S46 | Urgent Clojure patch release. The output shape is probably unchanged. If it changes, C01 gives policy fallback and a one-namespace fix. | all | yes | C01 (reuse) |
| S64 | JSON class files: Clojure itself stops. With C01 the probe reports `:unsupported-compiler`. Non-nil definitions fail, and both backends need a rewrite. | none useful | no | C01 (partial) |

### JVM-format group (valhalla-jvm, value-transform, cap-probe, array-adapter, jdk-internal-value)

| ID | Effect on design | Remaining part | Survives | Change |
|---|---|---|---|---|
| S05 | No new EA builds. Baseline fallback keeps F1–F4. F5 fails clearly. EA3 stays usable while it can be downloaded. | all except arrays | yes | — |
| S10 | 1e9 elements: lengths up to `Integer/MAX_VALUE` are allowed. The JVM gives a clear OOM. `into-array` buffers its input, so it needs about 2× memory. | all | yes | — |
| S19 | No `--add-exports` permitted: array capability is unavailable and fails clearly. Native fields need no export. | all except arrays | yes | — |
| S24 | Five EA builds at the same time: each build can have its own flags and version rule. These are hard-coded in two places (probe, transform). The matrix grows with each row. The effort exceeds the limit. | current build | naive: no → yes | C03, C04 |
| S32 | New `ACC_STRICT_INIT` and version rule. Naive: the probe gets a `ClassFormatError` (unknown, so it propagates) and every definition throws. The fix touches two namespaces. With C03 it is one table row. | baseline | yes | C03 (reuse) |
| S33 | JEP 401 final: no preview minor version. Naive: the probe gets a preview-version rejection, reports unavailable, and silent fallback gives identity classes on a JVM that supports value classes (silent wrong representation). With C03: a table entry for JDK 28; a lookup miss is reported as `:unknown-jvm-format`. | all | naive: no → yes | C03 (reuse) |
| S34 | NullRestricted replaced: the native-field probe reports unavailable and generated enforcement keeps F3. Flattening is lost (not essential). | all | yes | — |
| S37 | `ClassFile.of` signature changes: the value backend throws and the probe (ASM) still reports available. The fix is in `class-file`/`transform` (one boundary). With C02 the probe uses the same API and detects the change. | baseline | yes | C02 (reuse) |
| S40 | AOT files from another feature release: the JVM gives `UnsupportedClassVersionError` (documented; rebuild). Fallback AOT loads with its guard. | all except stale value AOT | yes | — |
| S54 | Four EA builds each year: each one needs assumption checks, two constant sites, a 9-minute matrix, and edits to 405 EA3 mentions in 204 files. With C03 and C04 the code and test cost is small. The documentation cost stays above the limit. | all | naive: no → yes | C03 (reuse), C04 (reuse), C05 |
| S60 | The verifier rejects all constructors: all of Clojure stops. Nothing remains. The real analogue, a changed value-constructor rule, becomes a C03 table entry. | none | no | C03 (partial) |
| S61 | Java 8 back-port: there is no classfile API, so the result is unavailable and fallback by policy. The report is true. The design does not claim this JVM. | all | yes | — |
| S73 | `Class.isValue` missing: `:missing-value-predicate`, fallback by policy, and a true report. | all | yes | — |

### Release group (release, source-jar)

| ID | Effect on design | Remaining part | Survives | Change |
|---|---|---|---|---|
| S13 | No publication: the repository is public, and the README installs from a clone (`:local/root`). | all | yes | — |
| S21 | Signed reproducible builds: consumers can build from source. Signing and fixed timestamps are a `build.clj`/`release.yml` change. | all | yes | — |
| S29 | Clojars closes: not published. Git dependencies work. | all | yes | — |
| S44 | Typosquat fork: README installs from the canonical Git repository. Clojars verifies reverse-domain groups. | all | yes | — |
| S50 | Partial upload: the workflow stops and documents manual inspection. The next commit gives a new version. | all | yes | — |
| S57 | Shallow clone: `fetch-depth: 0` and the release shallow-clone check reject it. | all | yes | — |
| S22 | No CI minutes: CI does not run the runtime suites. Hooks and local commands remain. | all | yes | — |
| S48 | Stolen GitHub account: Clojars credentials are GitHub secrets, so a bad JAR is published under the real coordinate. Consumers get wrong code silently (F7). | none safe | naive: no → yes | C06 |

### Other stressors (ID order)

| ID | Effect on design | Remaining part | Survives | Change |
|---|---|---|---|---|
| S03 | `defvaluetype*` loses its first user. The functions do not change. | all | yes | — |
| S16 | closed-record forks for per-type overrides (rejected in D10). value-type does not change. | all | yes | — |
| S17 | Merge into closed-record: the namespaces move. Consumers get them through closed-record. | all | yes | — |
| S23 | Each JVM row doubles the cells. With C04, extra rows are smoke rows. | all | yes | C04 (reuse) |
| S25 | AI price ×3: slower work. The maintainer can still verify and release. | all | yes | — |
| S30 | Scry abandoned: the tests use `clojure.test`, so another runner is a deps change (the cell harness is separate). | all | yes | — |
| S41 | `wran`: `impl.runtime` throws `IllegalArgumentException` at load, naming the valid values. Clear, early. | all | yes | — |
| S43 | Report keys renamed: no backward compatibility (AGENTS.md). The report stays true. Changelog. | all | yes | — |
| S47 | Unsafe nil write: outside the contract (documented). The constructor paths keep F3. | all | yes | — |
| S49 | Only EA3 copy stolen; EA3 cannot be downloaded: the claimed JVM can no longer be verified (F7). | code, baseline tests | naive: no → yes | C07 |
| S51 | ARM-only, EA only for x86: users fall back by policy. The maintainer machine has an aarch64 EA3. | all | yes | — |
| S53 | AI boycott: adoption falls. The functions do not change. | all | yes | — |
| S55 | No Java 8 in CI: use another non-Valhalla JVM as the baseline. With C05 this is a one-place change. C07 keeps Java 8 available. | all | yes | C05 (reuse), C07 (reuse) |
| S56 | 4-hour matrix: with C04 the full matrix runs only on the primary pair. | all | yes | C04 (reuse) |
| S59 | Every field `__hash`: duplicate names fail as in `deftype`. Real analogue: record-suffix detection rejects partial forms clearly (D2). | all | yes | — |
| S62 | Docs in Latin: restore from Git. | all | yes | — |
| S63 | Different property value per thread: the policy is read once at namespace load. | all | yes | — |
| S65 | Preview banned: fallback by policy. | all | yes | — |
| S66 | Managers forbid value-type: adoption. The functions do not change. | all | yes | — |
| S67 | Benchmark noise: benchmarks are not a gate. | all | yes | — |
| S68 | A bit flip in a cached result. available→true gives a clear transform error. →false gives silent identity until restart. A restart recomputes the result. | all after restart | yes | — |
| S70 | Replayed ordinary value expansion: no loader is installed in the new JVM, so `check-value-class` throws `:not-value-class`. The literal `installed=true` misleads. Non-nil expansions use receiving macros and work. | fallback and non-nil | naive: no → yes | C08 |
| S72 | Old benchmark cited as a guarantee: the README and the design disclaim this. | all | yes | — |

### Pass 3: stressors from the evaluation

Code facts at `5073893f`: the probe checks only `isValue` and one field read (`impl/capability.clj`). It does not check `==` or arrays. `impl.array` derives allocation capability from the value-class result. Value AOT output has no load-time guard. No property can switch off value classes on a capable JVM.

| ID | Effect on design | Remaining part | Survives | Change |
|---|---|---|---|---|
| S58 | All value objects are `==`. The probe passes. Every value definition gives a class with wrong `identical?` and default equality. Nothing detects it, and the user cannot switch to identity classes without a different JVM or no preview (F1, F6 lost silently). With C10 the probe sees two different probe objects as `==`, reports `:failed-self-check`, and definitions fall back by policy (correct identity semantics). Value AOT output fails at load with the same reason. | all (identity) | naive: no → yes | C09, C10 |
| S38 | A JIT defect gives wrong values from flattened arrays. The defect appears only in compiled code, so a load-time self-check (C10) does not see it. With C11 the defect is found before the build is claimed, if a test exercises it. After detection, C09 switches off value classes and arrays by one property (configuration only). A defect that no test exercises stays silent until a user reports it. | all after detection | partial | C09, C10 (partial), C11 |

## 2. Changes

| ID | Description | Type | Elements | Stressors |
|---|---|---|---|---|
| C01 | **Compiler boundary.** A new namespace owns the model of compiler output (constructor shape, field order, record suffix). `value-transform` and `identity-backend` read it. The capability result adds a compiler-integration check, once per runtime: capture and shape-check a probe `deftype`. A failure gives value-class capability unavailable with reason `:unsupported-compiler`, then fallback by policy. Non-nil definitions fail with the same reason. | move a boundary; make behaviour predictable | clj-compiler, loader, value-transform, identity-backend, cap-probe, capability-report | S26, S28 (partial), S46, S64 (partial) |
| C02 | **Probe without clojure.asm.** Build the probe class with `java.lang.classfile`. The probe runs only after the API is found. The public namespaces then load without `clojure.asm`. `identity-backend` stays lazily resolved. Merged into C03 at consolidation. | remove a dependency | cap-probe, clojure-asm | S27, S37 |
| C03 | **JVM format table.** A new namespace owns the JEP 401 flag values, the version rule and the value-constructor order rule, keyed by feature release or build. The probe and the transform both read it. A lookup miss gives reason `:unknown-jvm-format`. Adding a build is one row. | make behaviour predictable; move a boundary | cap-probe, value-transform, valhalla-jvm, aot-output, capability-report | S24, S32, S33, S54, S60 (partial) |
| C04 | **Tiered test matrix.** Run the full matrix on one primary pair (Java 8 baseline, current EA, preview on and off). Each additional JVM gets a smoke row: load, define, policy, one AOT round trip. | change infrastructure | test-matrix, quality-ci, maintainer | S23, S24, S54, S56 |
| C05 | **One source of supported-JVM facts.** One data file holds the tested JVMs, build IDs, flags, download URL and SHA. Tests read it. Docs link to it and do not repeat build IDs. | make behaviour predictable; process | docs, test-matrix, valhalla-jvm, baseline-jvm | S54, S55 |
| C06 | **Release signature outside GitHub.** Sign release artifacts with a key that is not stored in GitHub. CI holds no publish credential, or the publish step needs the offline signature. Document how to verify. | change a process | release, quality-ci, maintainer, source-jar | S48 |
| C07 | **Archive tested JDKs.** Keep a private, checksummed copy of each JDK build in the C05 table. | change a process | valhalla-jvm, baseline-jvm, test-matrix, maintainer | S49, S55 (also helps S05) |
| C08 | **Receiving expansion for all definitions.** Ordinary value definitions expand to a receiving macro, as non-nil fields already do, so the capture loader installs where the form is analysed. Removes the `installed` literal and the second expansion style. | make behaviour predictable; fewer branches | core-macro, loader, expansion-transfer, tooling | S70 (also the tooling `macroexpand` risk in `risks-and-evolution.md`) |
| C09 | **Value-class switch.** A JVM property `value-type.value-classes` (`auto`, `off`), read once at load like the fallback policy. An invalid value throws at load. `off` gives value-class capability unavailable with reason `:disabled`. Native fields and array allocation derive from it, so they are also unavailable. Definitions fall back by policy. Arrays fail clearly. | make behaviour predictable | runtime-policy, cap-probe, array-adapter, jvm-flags, capability-report, docs | S38, S58 |
| C10 | **Semantic self-check.** The probe checks value semantics, not only `isValue`: two probe objects with equal fields are `==`, two with different fields are not. The array capability allocates a small null-restricted array, writes it, and reads it back. A failure gives reason `:failed-self-check`, then fallback by policy (values) or a clear failure (arrays). Value AOT output checks the cached result at namespace initialization and throws with the reason. | add a function | cap-probe, array-adapter, aot-output, core-macro, capability-report | S58, S38 (partial) |
| C11 | **Compiled-code test row.** The primary pair of C04 adds one row that runs the value and array suites with forced JIT compilation. A new EA build enters `jvm-facts` (C05) only after this row passes. | change infrastructure | test-matrix, jvm-facts, valhalla-jvm, maintainer | S38 |

## 3. Consolidation (step 6)

- **C02 merged into C03.** The probe builds its class through the C03 format namespace with `java.lang.classfile`. One boundary then owns everything that changes with the EA build: format rules, probe, value transform. This is the JVM-format group of `coupling.md`.
- **C01 aligns with the compiler group.** `loader`, `identity-backend` and the compiler-shape model form one boundary, the only one that knows compiler output. This shows hidden link 1 of `coupling.md` in the design.
- **C04, C05 and C07 share one data source.** The C05 table selects the C04 rows and names the C07 archives.
- **C08 removes a branch.** One expansion style for all definitions.
- No two-way dependencies were found or added. No links removed: every link is used by a function.
- Pass 3: C10 goes inside the JVM-format boundary (probe) and the Arrays boundary. C09 goes inside the Policy boundary: the policy decides what happens when capability is absent, and C09 makes it absent. C11 is one more row in the C04 tiers, selected from the C05 table. C10's AOT check uses the C08 receiving expansion, so it adds no expansion style.

## 4. Check again (step 7)

Pass 2: all 55 training stressors applied to the consolidated design (`adapted.md`).

- No new failures from the changes. Checked:
  - C01: the probe runs where defvaluetype runs, so the AOT and native-image paths (S35, S45) do not change.
  - C08: the AOT fallback guard does not change.
  - C03: the probe and the transform agree by construction.
- No stressor needed a new change. The procedure stops after pass 2.

Pass 3 check: all 57 stressors (55 training, S38, S58) applied to the design with C09–C11.

- No new failures. Checked:
  - S41, S63: the C09 property is read once and rejects invalid values at load, as the policy does.
  - S35, S45: AOT identity output does not run the probe, so C10 does not change it. Value AOT output now runs the probe at initialization (open decision 10).
  - S68: a bit flip in the cached result does not change (one more key).
  - S65: preview banned gives fallback before the self-check runs.
- S38 stays partial. A smaller change that detects JIT-only defects at run time was not found: a check of each array read is too expensive and cannot be complete.

## 5. Open decisions (trade-offs for the user)

1. **C01 converts compiler defects into fallback.** Under the default `silent` policy, a Clojure change gives identity classes with no message. The present rule is "unknown failures propagate" (defect visibility). Options: (a) `:unsupported-compiler` only for known shape mismatches; other failures propagate. (b) Always warn for this reason, even under `silent`. (c) Accept it.
2. **C01 probe cost.** One probe `deftype` compiled at first use: startup time and one class in the `DynamicClassLoader` cache.
3. **C03 fails closed on unknown JVMs.** Today `latestMajorVersion` + preview minor works on a new build when the format does not change. With a table, an unknown build gives no value classes until a row is added. The trade-off is predictability against zero-effort support of compatible builds.
4. **C02/C03 and the identity backend.** The probe no longer needs `clojure.asm`, but `identity-backend` does. If Clojure removes it (S27), non-nil fallback stops until the backend moves to `org.ow2.asm`. Decide now whether to depend on `org.ow2.asm` (a new runtime dependency) or to accept the risk.
5. **C04 reduces evidence** for the JVMs that are not primary. The claims in the docs must say "smoke-tested".
6. **C05 makes docs less self-contained.** Readers follow a link to see the tested build.
7. **C06 adds key management** for one maintainer, and can end automated publication.
8. **C07 redistribution.** EA licences can forbid redistribution. Keep the archive private.
9. **C08 changes the expansion shape** of ordinary definitions. No backward compatibility is needed, but the transfer and AOT tests (a large part of `test-matrix`) change.
10. **C10 startup cost and AOT.** The self-check adds work to the first probe. Value AOT output now runs the probe at namespace initialization, so AOT applications pay the probe cost at startup.
11. **C09 under policy `error`.** `off` with policy `error` throws on each definition. Options: (a) accept and document "use `off` with `silent` or `warn`"; (b) `:disabled` is exempt from the policy.
12. **C11 matrix time.** Forced JIT compilation is slow. It adds time to the primary pair that C04 tries to keep short.

## 6. Failure modes of shared elements (step 9)

| Element | Used by | Technical failure modes |
|---|---|---|
| cap-probe | C01, C03, C09, C10, F1, F6 | A self-check that is too strict gives fallback on a good JVM (under `silent`, with no message). Probe defect → all value output lost; under `silent` with no message. Probe class leak in the static class cache (UUID names). A wrong reason classification hides defects (open decision 1). Delay poisoned by an exception thrown during first use. |
| format table (C03) | probe, transform | Wrong or stale row → the probe passes and the transform output is rejected (D9 wraps), or the probe fails on a good JVM. Two builds with one feature release need a build key, not only a major version. |
| loader / compiler boundary (C01) | all transformed paths | Proxy dispatch error. Binding left in a tooling frame. The shape model is out of date for a patch release. |
| test-matrix | C04, C05, F7 | Child-JVM isolation errors. Flaky cells. Two unresolved review items: label-order agreement and the loader-isolation negative check (`mementum/state.md`). Smoke rows miss defects that only the cross product finds. |
| maintainer | release, C04–C07 | Single person. C06 makes the signing key a second single point. |

## 7. Remaining failures

| ID | Reason |
|---|---|
| S28 | Capture ineffective: non-nil definitions need capture on both backends. A fix needs a new D3 design. |
| S60 | Absurd: no JVM class with a constructor can load. |
| S64 | Absurd: Clojure itself stops. Non-nil backends need a rewrite. |
| S38 | Partial: a JIT-only defect that no test exercises stays silent until reported. After detection, C09 gives a return by configuration. |
