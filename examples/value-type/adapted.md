# run: value-type-r1 | date: 2026-11-06 | skill: adapt-design

# Adapted design: value-type

Base: `naive.md`. Changes C01–C08 of `adaptation.md`, after consolidation (C02 merged into C03).
Markers: **[new]** a new element, **[changed]** a changed element or flow. Elements without a marker are as in `naive.md`.

## Summary

```text
defvaluetype / defvaluetype*                                  [changed C08]
  → validate fields
  → capability (probe through compiler boundary and format table)   [changed C01 C03]
      reasons: … | :unsupported-compiler | :unknown-jvm-format       [new]
  → application policy (unchanged)
  supported   → receiving macro (all definitions)                    [changed C08]
                → install capture loader → deftype
                → transform bytes (format table, compiler-shape model) [changed C01 C03]
                → write .class (AOT) → define and link → check value class
  unavailable → silent | warn | error (unchanged)
```

## Boundaries

| Boundary | Elements | Owns | Changes when |
|---|---|---|---|
| **Compiler boundary** [new, C01] | loader, identity-backend, compiler-shape [new] | Every assumption about Clojure compiler output: `Compiler/LOADER` capture, constructor shape, field order, record suffix. | Clojure changes `deftype`/`deftype*` output or `LOADER` binding. |
| **JVM-format boundary** [new, C03 + C02] | jvm-format [new], cap-probe [changed], value-transform [changed] | JEP 401 flags, version rule, value-constructor order rule, keyed by feature release or build. The probe uses the same table and `java.lang.classfile`; no `clojure.asm`. | A new EA build, or JEP 401 becomes final. |
| Public API | core-macro [changed C08], array-api, capability-report [changed: new reasons] | Syntax, policy entry, reports. | Public contract decisions. |
| Policy | runtime-policy | Fallback policy, warning flag, guards. | Unchanged. |
| Arrays | array-adapter, jdk-internal-value | Internal `ValueClass` access. | Unchanged. |
| **Supported-JVM facts** [new, C05] | jvm-facts [new] → test-matrix [changed C04], docs [changed], jdk-archive [new C07] | One data file: tested JVMs, build IDs, flags, URL, SHA, matrix tier. | A JVM is added or removed. |
| Delivery | source-jar, release [changed C06], quality-ci | JAR, signed publication. | Release process changes. |

## Elements (new or changed)

| id | Kind | Description | Change |
|---|---|---|---|
| compiler-shape | component **[new]** | Model of compiler output used by both backends and by the compiler-integration probe. | C01 |
| jvm-format | component **[new]** | JEP 401 format table; lookup by running feature release/build. | C03 |
| cap-probe | component **[changed]** | Probe class built through `jvm-format` with `java.lang.classfile` (no `clojure.asm`). Adds a once-per-runtime compiler-integration check through `loader` and `compiler-shape`. Reasons add `:unsupported-compiler`, `:unknown-jvm-format`. | C01, C02, C03 |
| value-transform | component **[changed]** | Reads constants and version rule from `jvm-format` and the constructor model from `compiler-shape`. No local constants. | C01, C03 |
| identity-backend | component **[changed]** | Reads the constructor model from `compiler-shape`. Still uses `clojure.asm` (open decision 4). | C01 |
| core-macro | component **[changed]** | All value expansions use a receiving macro. No `installed` literal. | C08 |
| capability-report | component **[changed]** | Reports the new reasons. | C01, C03 |
| jvm-facts | artifact **[new]** | Supported-JVM data file. Source for tests, matrix tiers, docs links, archive. | C05 |
| test-matrix | artifact **[changed]** | Full matrix on the primary pair. Smoke rows for other JVMs. Rows selected from `jvm-facts`. | C04, C05 |
| docs | artifact **[changed]** | Link to `jvm-facts`. No repeated build IDs. | C05 |
| jdk-archive | artifact **[new]** | Private checksummed copies of tested JDK builds. | C07 |
| release | process **[changed]** | Artifacts signed with a key not in GitHub. CI holds no publish credential, or publish needs the offline signature. | C06 |

All other elements: as in `naive.md`.

## Connections (from uses to)

Removed:
- `cap-probe → clojure-asm` (C02)

Added:
- `cap-probe → jvm-format`, `cap-probe → classfile-api`, `cap-probe → loader`, `cap-probe → compiler-shape` (C01, C03)
- `value-transform → jvm-format`, `value-transform → compiler-shape` (C01, C03)
- `identity-backend → compiler-shape` (C01)
- `compiler-shape → clj-compiler` (C01). This makes hidden link 1 of `coupling.md` explicit.
- `jvm-format → valhalla-jvm` (C03). The probe and the AOT output now meet in `jvm-format`. This makes hidden link 2 of `coupling.md` explicit.
- `test-matrix → jvm-facts`, `docs → jvm-facts`, `jvm-facts → jdk-archive` (C04, C05, C07)
- `release → signing key (outside GitHub)` (C06)

Unchanged: all other rows of `naive.md`. Two-way dependencies: none. (`cap-probe → loader` and `core-macro → loader` are one-way; `loader` does not use `cap-probe`.)

## Remaining failures

S28, S60, S64 (see `adaptation.md` section 7).
