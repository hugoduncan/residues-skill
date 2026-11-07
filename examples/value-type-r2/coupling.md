# run: value-type-r2 | date: 2026-11-06 | skill: find-hidden-coupling

# Hidden coupling: value-type (r2)

Input: `design.md`, `elements.tsv` (33 elements), `stressors.tsv` (93 training stressors; 31 test stressors not used), `connections.tsv` (77 rows, same as r1).
Command: `python3 skills/find-hidden-coupling/scripts/coupling.py examples/value-type-r2` (default limits: similarity ≥ 0.5, shared ≥ 3).
The default limits found no hidden pairs. Sensitivity check (step 3): the same command with `--min-similarity 0.35`, then `0.3`.

## 1. Changes to elements and mapping

None. Elements and connections are the same as r1.

## 2. Mapping check

Pass at all three limits. Top element: `maintainer`, 25/93 (27%). No stressor has an empty mapping. Coupled pairs: 2 (0.5), 4 (0.35), 7 (0.3) of 528.

## 3. Vulnerable elements and dangerous stressors

| Element | Training stressors |
|---|---|
| maintainer | 25 |
| docs | 23 |
| release | 22 |
| valhalla-jvm | 20 |
| user-code | 16 |
| cap-probe | 15 |
| test-matrix | 15 |

Dangerous stressors (5 elements each): S005 (value classes on every JVM), S009 (50000 types in one namespace), S013 (1000 REPL redefinitions), S031 (preview features dual-use), S039 (Clojure 1.10/1.11 support), S056 (module path), S097 (monthly Clojure releases).

## 4. Coupled pairs

Default limits (0.5 / 3):

| A | B | Shared | Similarity | In design | Stressors |
|---|---|---|---|---|---|
| array-adapter | array-api | 4 | 0.57 | yes | S014, S036, S052, S106 |
| clj-compiler | loader | 8 | 0.50 | yes | S009, S010, S013, S016, S039, S071, S097, S102 |

Sensitivity, 0.35 / 3 (added pairs):

| A | B | Shared | Similarity | In design | Stressors |
|---|---|---|---|---|---|
| release | source-jar | 11 | 0.48 | yes | S002, S027, S028, S034, S043, S050, S067, S082, S090, S095, S096 |
| ai-agents | maintainer | 9 | 0.36 | yes | S003, S021, S024, S040, S069, S078, S083, S085, S110 |

Sensitivity, 0.3 / 3 (added pairs):

| A | B | Shared | Similarity | In design | Stressors |
|---|---|---|---|---|---|
| clj-compiler | core-macro | 6 | 0.32 | yes | S009, S010, S013, S016, S101, S112 |
| app-author | jvm-flags | 4 | 0.31 | yes | S015, S031, S056, S093 |
| cap-probe | loader | 6 | 0.30 | **no (hidden)** | S008, S009, S057, S071, S102, S105 |

## 5. Groups and two-way dependencies

Default: two groups, one for each pair.

At 0.3: five groups. The only group with more than two elements is **cap-probe, clj-compiler, core-macro, loader**. Only S009 is shared by all four. The group is a chain through `loader`.

Two-way dependencies: none.

## 6. Boundary candidates

1. **cap-probe and loader both define classes through Clojure's `DynamicClassLoader`, and the design does not connect them** (S008, S009, S057, S071, S102, S105). The probe defines a class with a random UUID name in a new `DynamicClassLoader`. The loader installs a proxy of `DynamicClassLoader` and defines the user classes. Both depend on its class cache, on the name rules, and on permission to call `defineClass`. A change to any of these (S071 hidden classes only, S105 equal UUIDs, S102 long names, S057 class replay) changes both. Candidate: one boundary that owns class definition (name, define, cache), used by the probe and the loader.
2. **Compiler chain: clj-compiler, loader, core-macro** (S009, S010, S013, S016, S039, S097, S101, S112). All connected. Many Clojure-version stressors (S039, S097) touch `loader`, `value-transform` and `identity-backend` together. Candidate: one boundary for all assumptions about compiler output.
3. **Unique pattern: maintainer** (25 stressors; coupled only with `ai-agents`, which the maintainer directs). Organisation, money and physical stressors reach release, tests, docs and JVM tracking through one person. Candidate: separate boundary (second owner, or a procedure that another person or an agent can run).
4. **release–source-jar** (11 stressors): already connected. Strong and expected. No change indicated.
5. **array-adapter–array-api**, **app-author–jvm-flags**: already connected and expected.
6. **Links that no stressor pattern supports:** none considered for removal. Each link has a function.

## 7. Gaps

- `expansion-transfer` has no training stressor. Coverage added two (S116, S117), and the random split put both in the test set.
- Low coverage in training: `classfile-api` (1), `clojure-asm` (2), `closed-record` (2), `field-cap-probe` (2).
- Coarse elements: `docs` and `maintainer` are the top two. `docs` combines README, generated API, Ramora and Mementum.
