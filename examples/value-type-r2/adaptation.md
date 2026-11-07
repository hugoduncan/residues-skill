# run: value-type-r2 | date: 2026-11-06 | skill: adapt-design

# Adaptation: value-type (r2)

Inputs: `naive.md`, `criteria.md` (copied from r1, confirmed 2026-11-06), `coupling.md`, 93 training stressors. The test stressors were not used. Bias: the same agent wrote the stressors and did run r1 (see `design.md`).

Code facts checked at commit `5073893f`:

- `impl/capability.clj`: imports `clojure.asm` at namespace load. Defines the probe class in a new `DynamicClassLoader` with a UUID name. Checks only `isValue` and one field read. Throws on an invariant failure.
- `impl/field_capability.clj`: also defines classes in a new `DynamicClassLoader` with UUID names. If the JVM accepts null in the `NullRestricted` field, the probe throws ("accepted null"). It does not report unavailable. (r1 adaptation S34 assumed "reports unavailable".)
- `impl/loader.clj`: proxy of `DynamicClassLoader`; writes class files when `*compile-files*` is true.
- `impl/runtime.clj`: policy read once at namespace load; no later check.
- `.github/workflows/release.yml`: manual dispatch from `master`, concurrency group `release`. Downloads Java 8 and EA3 with fixed SHA-256 checks. Runs all runtime, fallback, cross-JVM, build and release suites before the JAR build. Clojars credentials are GitHub secrets.
- `.github/workflows/ci.yml` (each push): format, lint, prose, API docs, tooling and release-contract tests. No runtime or fallback suite.
- `README.md`: install from a clone of the repository (`:local/root`). Not published on Clojars.
- `doc/usage.md`: identity operations on value objects throw `IdentityException`. Serialization is excluded from the guarantees.

Order: coupling groups first (class definition, compiler chain, maintainer, release, arrays, operator configuration), then the other stressors in ID order.
"Survives" refers to the design at that point, with the earlier changes. `naive: no` shows that the naive design does not survive.

## 1. Stressor results

### Class definition group (cap-probe, loader; hidden at 0.3)

| ID | Effect on design | Remaining part | Survives | Change |
|---|---|---|---|---|
| S008 | A plugin depends on private namespaces. They have no contract (no backward compatibility). The functions do not change. | all | yes | — |
| S009 | 50000 definitions: one probe for each runtime, one capture loader for each form. Class count and namespace size limits are the same as for `deftype`. | all | yes | — |
| S057 | Leyden caches classes from built-in loaders. Classes from `DynamicClassLoader` are defined as before. The capability result is in a `delay`, which is not cached. | all | yes | — |
| S071 | `defineClass` forbidden: Clojure source loading also stops. AOT value and fallback output load from the class path. | AOT path | yes | — |
| S102 | 1 MB class names: no class can be defined, also not by the JVM or Clojure. Nothing remains. No library change can help. | none | no | — |
| S105 | Equal UUIDs: each probe runs once for each runtime, and the value and field probes use different prefixes. Names do not collide. | all | yes | — |

### Compiler chain (clj-compiler, loader, core-macro)

| ID | Effect on design | Remaining part | Survives | Change |
|---|---|---|---|---|
| S010 | `*compile-files*` rebound: the capture loader writes class files exactly when `deftype` would. | all | yes | — |
| S013 | 1000 redefinitions: each form gets a new capture loader and class, as `deftype` does. The probe result is cached. | all | yes | — |
| S016 | A protocol extension before the type exists fails with a clear "class not found", as for `deftype`. | all | yes | — |
| S039 | Clojure 1.10/1.11: the design knows only 1.12.6 output. An application can override the Clojure version. Then the shape check fails and every value and non-nil definition throws, under all policies. Support needs changes in `loader`, `value-transform`, `identity-backend` and `core-macro`: more than one boundary. | baseline, ordinary definitions | naive: no → yes | C01 |
| S097 | A new Clojure minor version each month: each one can change compiler output. With C01, one namespace changes, and a failed compiler check gives fallback by policy. C03 shows each output change as a text diff. | all | naive: no → yes | C01 (reuse), C03 (reuse) |
| S101 | Absurd: the reader turns `defvaluetype` into `defrecord`. value-type never runs. Nothing in the library can detect it. | none of the library | no | — |
| S112 | Case-insensitive symbols: duplicate fields fail as in `deftype`. | all | yes | — |
| S114 | The `ClassWriter` constructor is removed: `impl.capability` does not compile when it loads, so the public namespaces do not load on any JVM (F4, F1 lost). `identity-backend` also uses it. | none | naive: no → yes | C02 |
| S123 | `clojure.asm` removed in one country: Clojure cannot compile source. AOT applications still run, but `impl.capability` imports `clojure.asm`, so value-type does not load (F4). With C02 it loads, and AOT output works. | AOT applications | naive: no → yes | C02 (reuse) |

### Maintainer group (maintainer, ai-agents)

| ID | Effect on design | Remaining part | Survives | Change |
|---|---|---|---|---|
| S003 | No downloads. The functions do not change. | all | yes | — |
| S021 | Out-of-date design reasons: tests and the generated API check keep the behaviour. History is in Git. | all | yes | — |
| S024 | No AI-written code: work is slower. Anybody can run the documented tasks to verify. | all | yes | — |
| S040 | Slow AI: work is slower. | all | yes | — |
| S069 | A hidden transform step: the transform works on bytes, so a review of the source diff does not show the change in output. Tests check behaviour, not bytes. A conditional payload passes review and tests, and reaches consumers (F7). With C03, each change of emitted bytes for the corpus is a text diff in the pull request. | all | naive: no → yes | C03 |
| S078 | Six months without the maintainer: the public repository and tasks remain. | all | yes | — |
| S083 | Time zone: slower review. | all | yes | — |
| S085 | Strike against AI training: no effect on the functions. | all | yes | — |
| S110 | 1000 maintainers: the release workflow is manual and serialised (concurrency group). | all | yes | — |

### Release group (release, source-jar)

| ID | Effect on design | Remaining part | Survives | Change |
|---|---|---|---|---|
| S002 | Purchase: published EPL code stays available in clones and forks. | all | yes | — |
| S027 | SBOM: a `build.clj`/`release.yml` change (one boundary). | all | yes | — |
| S028 | EPL invalid in one country: the copyright holder can relicense (documentation). | all | yes | — |
| S034 | Clojars charges: the README installs from the repository. | all | yes | — |
| S043 | deps-deploy abandoned: replace one release step. | all | yes | — |
| S050 | GitHub down for one month: the repository is the only channel. New consumers cannot get the library (F7). CI and release stop. With C04, Clojars and a mirror carry each release. | all (C04) | naive: no → yes | C04 |
| S067 | History rewrite: the version number goes down. Clojars refuses an existing release version, so publication fails clearly. | all | yes | — |
| S082 | Clojars mirror down: the repository channel remains. | all | yes | — |
| S090 | Clojars blocked: the repository channel remains. | all | yes | — |
| S095 | Two release runs: concurrency group `release` serialises them. Each commit has its own version. | all | yes | — |
| S096 | Timestamps go backwards: the version does not use time. If Clojure loads source instead of stale AOT classes, the result is decided again by policy on the same JVM. | all | yes | — |

### Arrays (array-api, array-adapter)

| ID | Effect on design | Remaining part | Survives | Change |
|---|---|---|---|---|
| S014 | Arrays from another loader: inspection uses static `ValueClass` methods and `isValue`. The loader is not relevant. | all | yes | — |
| S036 | Sponsor for arrays only: the functions do not change. | all | yes | — |
| S052 | Allocator removed in a new build: `:missing-array-signature`, arrays fail clearly. The build is not claimed. | all except arrays | yes | — |
| S106 | Absurd: all arrays have length 0. The JVM and Clojure stop. | none | no | — |

### Operator configuration (app-author, jvm-flags)

| ID | Effect on design | Remaining part | Survives | Change |
|---|---|---|---|---|
| S015 | Policy `error` and fallback AOT in a dependency: the guard throws `Error` at namespace initialization. Clear and early. This is the design (F2). | all | yes | — |
| S031 | No preview, no internal packages: fallback by policy; arrays fail clearly. | all except arrays | yes | — |
| S056 | Module path: `--add-exports …=ALL-UNNAMED` does not reach an automatic module, so arrays fail clearly with `:array-access-denied`. The message names the unnamed-module flag. Fix: documentation of the module name. | all except arrays | yes | — |
| S093 | The property is set after load: the policy is read once, so the new value is ignored with no message. An application that sets `error` gets silent fallback. A strict failure is skipped silently (F2). With C05 the first fallback decision sees the difference and warns. | all | naive: no → yes | C05 |

### Other stressors (ID order)

| ID | Effect on design | Remaining part | Survives | Change |
|---|---|---|---|---|
| S001 | Kotlin value classes: compile-time wrappers, usable as ordinary classes. A new feature, not a lost function. | all | yes | — |
| S005 | Value classes everywhere: the identity backend and Java 8 rows become unused. The functions remain. | all | yes | — |
| S011 | RMI to a fallback JVM: serialization is excluded. The class shapes differ, so deserialization fails clearly. | all | yes | — |
| S012 | Weak keys: `IdentityException` (documented). Fallback objects work. | all | yes | — |
| S017 | Java 21: no `java.lang.classfile`, so `:missing-classfile-api` and fallback by policy. | all | yes | — |
| S018 | Slow reviews: slower work. | all | yes | — |
| S023 | A merge disables the `error` policy. The release workflow runs the fallback suites and stops. But consumers install from a clone of `master`, and CI on push does not run these suites. Consumers get the change silently (F2). With C06, consumers install only tested release tags. | all | naive: no → yes | C06 |
| S026 | Security promise for paid maintainers: the maintainer is not paid. | all | yes | — |
| S032 | Trademark: rename in documentation only. | all | yes | — |
| S033 | Capability audit log: a change inside `impl.runtime` (one boundary). | all | yes | — |
| S035 | Smaller machine: suites run in sequence, slower. The release workflow runs them in CI. | all | yes | — |
| S037 | Cheap memory: less value of the library. The functions remain. | all | yes | — |
| S038 | GitHub storage charges: the release goes to Clojars, not to GitHub storage. | all | yes | — |
| S041 | EA3 for five years: EA builds disappear from the download site. The design keeps no copy. After removal, nobody can verify on EA3 (F7). | code, baseline tests | naive: no → yes | C07 |
| S042 | No macOS EA builds: run the Valhalla suites on Linux (CI, container). | all | yes | — |
| S044 | clj-kondo hooks fail: lint configuration change. | all | yes | — |
| S047 | Vale rules: pin the version or change the configuration. | all | yes | — |
| S049 | quickdoc abandoned: the pinned version keeps working. | all | yes | — |
| S051 | `-XX:-ValueClasses` on a new build: the probe class is defined but is not a value class. The invariant check throws, so definitions throw under all policies. The flag is on a build that is not claimed. The fix (classify as unavailable) is one namespace. | all after a fix | yes | — |
| S053 | `==` on floats compares bits: JVM semantics. The docs say that equality depends on fields. | all | yes | — |
| S055 | 64-field limit: a larger value class is rejected (`:jvm-rejected`, with the JVM message). Clear, early, names the limit. | all | yes | — |
| S058 | New major version in one release: the probe and the transform read `latestMajorVersion` at run time. Old value AOT output fails with `UnsupportedClassVersionError` (documented: rebuild). | all | yes | — |
| S060 | Babashka: SCI has its own implementation. value-type does not change. | all | yes | — |
| S061 | Renamed tag class: `NoClassDefFoundError`, as for `deftype`. | all | yes | — |
| S062 | Datomic: stored values do not depend on the representation. Reader functions construct the class that exists. | all | yes | — |
| S063 | Printed form as key: identity objects already print an identity hash. Not a contract. | all | yes | — |
| S064 | Wrong documented SHA: `release.yml` checks its own SHA against the download, so a mismatch stops the release clearly. Users who check the docs see a mismatch. | all | yes | — |
| S066 | `readObject` and nil: serialization is excluded. Constructor paths keep F3. | all | yes | — |
| S068 | Corrupted fixture: Git detects corruption. A failing case shows in the suites. | all | yes | — |
| S070 | Replaced closed-record: value-type does not change. Dependency resolution selects the newer value-type. | all | yes | — |
| S072 | Hash flooding: user hash design, as for records. | all | yes | — |
| S074 | Compromised runner: the release job holds the Clojars credentials. The runner can change the JAR before publication. Consumers get wrong code silently (F7). With C08, consumers verify a signature made outside GitHub. | none safe | naive: no → yes | C08 |
| S076 | Trojan EA build: the release JAR is source-only and built in CI from Git. The maintainer's machine is at risk, not the artifact. | all | yes | — |
| S077 | Flood: the code is in GitHub. A new machine downloads the tools. C07 keeps the JDK copies off-site. | all | yes | C07 (reuse) |
| S079 | Two weeks offline: support for a new build is late. The claimed build stays supported. | all | yes | — |
| S080 | Corrupted JAR in the CI cache: the build fails clearly. Clear the cache. | all | yes | — |
| S081 | 64 MB devices: no Valhalla EA build; fallback by policy. | all | yes | — |
| S087 | Campaign against preview: adoption. The functions remain. | all | yes | — |
| S088 | National JVM without Valhalla: fallback by policy. | all | yes | — |
| S089 | False claim: documentation and tests answer it. | all | yes | — |
| S091 | Twenty years of EA builds: each build changes flags and the version rule, which are hard-coded in two namespaces. Build IDs are repeated in many documents. Each build costs more than the acceptable effort, for twenty years. With C09 a build is one table row. With C10 documents link to one data file. | all | naive: no → yes | C09, C10 |
| S098 | Ten-year-old AOT application: it runs on its JVM. On a new JVM, `UnsupportedClassVersionError` (documented). | all | yes | — |
| S100 | Absurd: all value objects of one class share one memory location. The probe checks one object, so it passes. Every value object has wrong field values, silently (F1, F6). With C11 the probe sees two objects with different fields read the same value, and reports `:failed-self-check`. Fallback by policy gives identity classes, which are correct. | all (identity) | naive: no → yes | C11 |
| S104 | Absurd: classes named "Probe" are refused. The probe error propagates (designed: unknown probe failures propagate). AOT output works. | AOT path | yes | — |
| S111 | Property varies on each read: read once, so the policy is stable. | all | yes | — |
| S113 | `java.lang.classfile` not resolved: `:missing-classfile-api`, fallback by policy. `--add-modules` returns it (configuration). | all | yes | — |
| S118 | `NullRestricted` removed on a new build: the field probe throws "accepted null", so non-nil value definitions throw. The build is not claimed. The fix (classify as unavailable) is one namespace. | all after a fix | yes | — |
| S119 | Fire: benchmarks are not a gate. The release runs in CI. | all | yes | — |
| S120 | Bad benchmark blog: the docs disclaim performance. | all | yes | — |
| S124 | Bit flip in the field-probe class after the probe: the result is cached; the class is not used again. | all | yes | — |

## 2. Changes

| ID | Description | Type | Elements | Stressors |
|---|---|---|---|---|
| C01 | **Compiler boundary.** One namespace owns the model of Clojure compiler output (constructor shape, field order, record suffix, `LOADER` capture) and all class definition through `DynamicClassLoader`. `loader`, both backends and the probes use it. The capability result adds a compiler check, once for each runtime: capture and shape-check a probe `deftype`. A failure gives `:unsupported-compiler`, then fallback by policy. | move a boundary; make behaviour predictable | clj-compiler, loader, value-transform, identity-backend, cap-probe, field-cap-probe, core-macro | S039, S097 |
| C02 | **No `clojure.asm`.** The probe builds its class with `java.lang.classfile`, only after the API is found. The identity backend uses a pinned `org.ow2.asm` dependency. | remove a dependency | cap-probe, identity-backend, clojure-asm, source-jar | S114, S123 |
| C03 | **Output snapshots.** For each case of the compatibility corpus, a committed text disassembly of the emitted classes. A test compares them. A change of emitted bytes is a text diff in review. | make behaviour predictable | test-matrix, value-transform, identity-backend, quality-ci | S069, S097 |
| C04 | **Two channels.** Each release goes to Clojars and to a mirror of the repository on a second host. | change a process | release, source-jar, lib-author | S050 |
| C05 | **Policy drift warning.** At each fallback decision, read `value-type.fallback` again. If it differs from the value read at load, warn once on stderr, under all policies, and name the value that applies. | make behaviour predictable | runtime-policy, jvm-flags, app-author | S093 |
| C06 | **Install tested releases.** The README installs a release tag (`:git/tag` and `:git/sha`) or the Clojars version, not a clone of `master`. Only the release workflow creates tags, after all suites pass. | change a process | docs, release, lib-author | S023 |
| C07 | **Archive tested JDKs.** Keep a private, off-site, checksummed copy of each JDK build that the release workflow uses. | change a process | valhalla-jvm, baseline-jvm, test-matrix, maintainer | S041, S077 |
| C08 | **Release signature outside GitHub.** The maintainer signs each release tag and artifact with a key that is not in GitHub. The README tells how to verify. | change a process | release, source-jar, maintainer, quality-ci | S074 |
| C09 | **JVM format table.** One namespace owns the JEP 401 flag values and the version rule, keyed by feature release or build. The probe and the transform read it. A lookup miss gives `:unknown-jvm-format`. | make behaviour predictable; move a boundary | cap-probe, value-transform, valhalla-jvm, aot-output | S091 |
| C10 | **One source of supported-JVM facts.** One data file: tested JVMs, build IDs, URLs, SHA-256. `release.yml`, tests and the archive (C07) read it. Documents link to it. | make behaviour predictable | docs, test-matrix, release, valhalla-jvm, baseline-jvm | S091 |
| C11 | **Semantic self-check.** The probe makes two objects with different field values and checks: each reads its own value; they are not `==`; two objects with equal fields are `==`. A failure gives `:failed-self-check`, then fallback by policy. | add a function | cap-probe, capability-report | S100 |

## 3. Consolidation (step 6)

- **C01 contains the hidden link of `coupling.md`.** The probes and the loader both define classes through `DynamicClassLoader`. C01 gives them one define function inside the compiler boundary. No training stressor broke this link, but S071, S102 and S105 now change one place.
- **C02, C09 and C11 share the probe.** The probe uses `java.lang.classfile` (C02) and the format table (C09), and runs the self-check (C11). One boundary owns everything that changes with the EA build.
- **C04, C06 and C08 form one release boundary:** tested, signed releases on two channels. The README installs only such a release.
- **C07 and C10 share one data file.** The C10 table names the C07 archive entries.
- **C03 supports C01.** The snapshots show when compiler output changes.
- No two-way dependencies found or added. No links removed: every link is used by a function.

## 4. Check again (step 7)

Pass 2: all 93 training stressors applied to the consolidated design (`adapted.md`).

- No new failure. Checked:
  - S058 with C09: a new major version that is not in the table gives `:unknown-jvm-format` and fallback until a row is added. This is loss of value output on a build that is not claimed (acceptable). Naive behaviour was better (open decision 8).
  - S111 with C05: a property that changes on each read makes C05 warn once. Not a failure.
  - S077 with C08: the signing key can be lost with the machines. Return: a new key, announced in the repository (days). Survives (open decision 7).
  - S009, S013, S105 with C01 and C11: the compiler check and the self-check run once for each runtime. Probe names keep different prefixes.
  - S050 with C06: the tag is on GitHub; the Clojars channel of C04 remains.
- No stressor needed a new change. The procedure stops after pass 2.

## 5. Open decisions (trade-offs for the user)

1. **C01 converts compiler defects into fallback.** Under `silent`, a Clojure change gives identity classes with no message. Today unknown failures propagate.
2. **C02 adds a runtime dependency** (`org.ow2.asm`), or keeps the risk of `clojure.asm` in the identity backend.
3. **C03 snapshot cost.** Each intended transform change, and each Clojure or JDK update, changes snapshots.
4. **C04 publication credential.** Clojars publication puts a credential in the release path (see C08).
5. **C06 delays fixes** for users who now take `master`. The README must name the current tag.
6. **C07 redistribution.** EA licences can forbid redistribution. Keep the archive private.
7. **C08 key management** for one maintainer. Keep an off-site key backup (S077).
8. **C09 fails closed** on unknown builds. Compatible new builds give no value classes until a row is added.
9. **C10 makes documents less self-contained.**
10. **C11 startup cost**, and a too-strict check gives fallback on a good JVM.
11. **C05 warns under `silent`.** This is against the meaning of `silent`, but the case is an application that wanted another policy.

## 6. Failure modes of shared elements (step 9)

| Element | Used by | Technical failure modes |
|---|---|---|
| cap-probe | C01, C02, C09, C11, F1, F6 | Probe defect → all value output lost; under `silent` with no message. Wrong reason classification hides defects. A too-strict self-check. Probe classes stay in the `DynamicClassLoader` cache. |
| compiler boundary (C01) | loader, backends, probes | Out-of-date shape model after a patch release. One define function is a single point for all class definition. |
| format table (C09) | probe, transform | Wrong or stale row → probe passes and output is rejected, or probe fails on a good JVM. |
| release (C04, C06, C08) | consumers, F7 | Tag and artifact disagree. Signature check not done by consumers. Mirror out of date. |
| test-matrix (C03, C10) | F7 | Snapshot churn hides a malicious change in a large diff. Child-JVM isolation errors. |
| maintainer | release, C07, C08 | Single person, and holder of the only signing key. |

## 7. Remaining failures

| ID | Reason |
|---|---|
| S101 | Absurd: the reader changes the form before value-type runs. |
| S102 | Absurd: no class can be defined. |
| S106 | Absurd: the JVM and Clojure stop. |
