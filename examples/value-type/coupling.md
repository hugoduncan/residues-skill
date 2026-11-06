# run: value-type-r1 | date: 2026-11-06 | skill: find-hidden-coupling

# Hidden coupling: value-type

Input: `design.md`, `elements.tsv` (33 elements), `stressors.tsv` (55 training stressors; 18 test stressors not used), `connections.tsv` (77 rows).
Command: `python3 skills/find-hidden-coupling/scripts/coupling.py examples/value-type` (default limits: similarity ≥ 0.5, shared ≥ 3).
Supplementary: the same command with `--min-similarity 0.35` and `--min-similarity 0.3`. The default limits apply (≥ 20 stressors). The lower limits are a sensitivity check only.

## 1. Changes to elements and mapping

None. Elements are already unique. No vague element was split. Two elements are coarse (see section 7).

## 2. Mapping check

Pass at all three limits. Top element: `test-matrix`, 13/55 (24%). No stressor has an empty mapping. Coupled pairs at default: 3 of 528.

## 3. Vulnerable elements and dangerous stressors

| Element | Training stressors |
|---|---|
| test-matrix | 13 |
| valhalla-jvm | 12 |
| value-transform | 12 |
| cap-probe | 11 |
| clj-compiler | 11 |
| docs | 11 |
| maintainer | 10 |
| release | 10 |

| ID | Elements | Stressor |
|---|---|---|
| S05 | 8 | Oracle stops Project Valhalla. |
| S33 | 7 | JEP 401 becomes final; no preview minor version, no `--enable-preview`. |
| S26 | 6 | Clojure 1.13 adds a hidden field and changes constructor order. |
| S32 | 6 | A new EA build changes `ACC_STRICT_INIT` and the version rule. |
| S54 | 6 | Each EA build lasts three months; four builds each year. |

## 4. Coupled pairs

Default limits (0.5 / 3):

| A | B | Shared | Similarity | In design | Stressors |
|---|---|---|---|---|---|
| release | source-jar | 6 | 0.60 | yes | S13, S21, S29, S44, S50, S57 |
| array-adapter | jdk-internal-value | 3 | 0.60 | yes | S05, S10, S19 |
| clj-compiler | loader | 7 | 0.58 | yes | S15, S26, S28, S35, S39, S45, S69 |

Supplementary (0.35 / 3, and 0.3 / 3). Only the hidden pairs are shown:

| A | B | Shared | Similarity | In design | Stressors |
|---|---|---|---|---|---|
| clj-compiler | identity-backend | 5 | 0.36 | no (hidden) | S06, S26, S27, S46, S64 |
| aot-output | cap-probe | 4 | 0.31 | no (hidden) | S32, S33, S35, S54 |

Other supplementary pairs, all in the design: closed-record–core-macro (0.40), baseline-jvm–identity-backend, clojure-asm–identity-backend, expansion-transfer–loader (0.38), cap-probe–valhalla-jvm (0.35), valhalla-jvm–value-transform, classfile-api–value-transform, core-macro–expansion-transfer (0.33), test-matrix–valhalla-jvm (0.32), app-author–jvm-flags (0.30).

## 5. Groups and two-way dependencies

Default: three groups, one per pair above.

At 0.3 there are two larger groups:

- **JVM-format group:** valhalla-jvm, value-transform, cap-probe, classfile-api, aot-output, test-matrix. One stressor (S32) is shared by all.
- **Compiler group:** clj-compiler, loader, identity-backend, clojure-asm, baseline-jvm, expansion-transfer, core-macro, closed-record. No stressor is shared by all. The group is a chain through `loader` and `identity-backend`.

Two-way dependencies: none.

## 6. Boundary candidates

1. **identity-backend depends on the Clojure compiler, and the design does not show it** (S06, S26, S27, S46, S64). The design connects `identity-backend` only to `clojure-asm`, `fields` and `baseline-jvm`. It also depends on the constructor shape that the compiler emits, and on the ASM fork that Clojure bundles. A change of the Clojure version therefore changes it through two paths. Candidate: show the link, or put `identity-backend` in the same boundary as `loader` (both are compiler-coupled).
2. **The probe and the AOT output share the class-file version rule** (S32, S33, S35, S54). `cap-probe` and `value-transform` each encode the flag values and the version rule (runtime embodiment, "Boundaries"). `aot-output` stores the result. Nothing in the design links the probe to the AOT artifacts. Candidate: one boundary that owns the format constants and the version rule, used by both the probe and the transform.
3. **JVM-format group** (S05, S24, S32, S33, S54): five components change together when the EA build changes. Candidate: put them inside one replaceable boundary ("EA adapter"), with the test rows that pin it.
4. **Unique pattern: maintainer** (10 stressors, no coupled partner). Organisation stressors reach release, tests, docs and JVM tracking only through one person. Candidate: separate boundary (a second owner or a documented, agent-runnable procedure). Stressors: S13, S15, S17, S23, S24, S25, S48, S49, S56, S67.
5. **release–source-jar** (S13, S21, S29, S44, S50, S57): already connected. The coupling is strong and expected. No boundary change is indicated.
6. **Links that no stressor pattern supports:** `quality-ci → core-macro` and `benchmarks → core-macro` have no shared stressor. Do not remove them: the API docs and benchmarks need these links.

## 7. Gaps

- Low coverage: `array-api` (1 training stressor), `tooling` (1). The array subsystem is coupled through `array-adapter`, so its coupling is under-sampled.
- Coarse elements: `docs` combines README, generated API, Ramora and Mementum. `test-matrix` combines four suites and the compat corpus. Their counts (11, 13) can hide internal coupling.
- Result: at the component level, coupling follows the declared connections. The design's own risk analysis already makes most dependencies explicit. Two hidden links (1, 2) appear only below the default limit.
