# run: value-type-r2 | date: 2026-11-06 | skill: adapt-design

# Adapted design: value-type (r2)

Base: `naive.md`. Changes C01–C11 of `adaptation.md`, after consolidation.
Markers: **[new]** a new element, **[changed]** a changed element or flow. Elements without a marker are as in `naive.md`.

## Summary

```text
defvaluetype / defvaluetype*
  → validate fields
  → capability                                                    [changed]
      probe: java.lang.classfile (no clojure.asm)                 [C02]
             format table lookup                                  [C09]
             compiler check through the compiler boundary         [C01]
             semantic self-check (own values, ==)                 [C11]
      reasons: … | :unsupported-compiler | :unknown-jvm-format
               | :failed-self-check                               [new]
  → application policy (read once at load)
      fallback decision: property read again; warn once on drift  [C05]
  supported   → install capture loader (compiler boundary) → deftype   [changed C01]
                → transform bytes (format table, compiler-shape model)  [changed C01 C09]
                → write .class (AOT) → define and link → check value class
  unavailable → silent | warn | error (unchanged)

release: all suites pass → signed tag (key outside GitHub) → Clojars + mirror   [C04 C06 C08]
consumers install a signed release tag or the Clojars version                   [C06]
```

## Boundaries

| Boundary | Elements | Owns | Changes when |
|---|---|---|---|
| **Compiler boundary** [new, C01] | loader, compiler-shape [new], define function | Every assumption about Clojure compiler output, and all class definition through `DynamicClassLoader` (user classes and probe classes). | Clojure changes `deftype`/`deftype*` output, `LOADER` binding or `DynamicClassLoader`. |
| **JVM-format boundary** [new, C02 C09 C11] | jvm-format [new], cap-probe [changed], field-cap-probe, value-transform [changed] | JEP 401 flags and version rule; probe class built with `java.lang.classfile`; semantic self-check. | A new EA build, or JEP 401 becomes final. |
| Public API | core-macro, array-api, capability-report [changed: new reasons] | Syntax, policy entry, reports. | Public contract decisions. |
| Policy | runtime-policy [changed C05] | Fallback policy, drift warning, guards. | The application changes policy. |
| Arrays | array-adapter, jdk-internal-value | Internal `ValueClass` access. | Unchanged. |
| Identity output | identity-backend [changed C02] | Identity classes with generated checks, through pinned `org.ow2.asm`. | ASM changes. |
| **Supported-JVM facts** [new, C10] | jvm-facts [new] → release, test-matrix, docs, jdk-archive [new C07] | One data file: JVMs, build IDs, URLs, SHA-256. | A JVM is added or removed. |
| **Release** [changed, C04 C06 C08] | release, source-jar, signing key [new], mirror [new] | Tested, signed releases on two channels. | Release process changes. |

## Elements (new or changed)

| id | Kind | Description | Change |
|---|---|---|---|
| compiler-shape | component **[new]** | Model of compiler output and the one define function for `DynamicClassLoader`. Used by `loader`, both backends and the probes. | C01 |
| jvm-format | component **[new]** | JEP 401 format table; lookup by feature release or build. | C09 |
| cap-probe | component **[changed]** | Builds the probe with `java.lang.classfile` and `jvm-format`. Defines it through `compiler-shape`. Adds the compiler check (C01) and the semantic self-check (C11). | C01, C02, C09, C11 |
| field-cap-probe | component **[changed]** | Defines probe classes through `compiler-shape`. | C01 |
| value-transform | component **[changed]** | Reads constants from `jvm-format` and the constructor model from `compiler-shape`. | C01, C09 |
| identity-backend | component **[changed]** | Reads the constructor model from `compiler-shape`. Uses pinned `org.ow2.asm`, not `clojure.asm`. | C01, C02 |
| loader | component **[changed]** | Defines classes through `compiler-shape`. | C01 |
| runtime-policy | component **[changed]** | At each fallback decision, compares the property with the value read at load. Warns once on a difference. | C05 |
| capability-report | component **[changed]** | Reports the new reasons. | C01, C09, C11 |
| test-matrix | artifact **[changed]** | Adds disassembly snapshots for the compatibility corpus. Reads `jvm-facts`. | C03, C10 |
| jvm-facts | artifact **[new]** | Supported-JVM data file. | C10 |
| jdk-archive | artifact **[new]** | Private, off-site, checksummed JDK copies. | C07 |
| docs | artifact **[changed]** | README installs a signed release tag or the Clojars version, and tells how to verify. Links to `jvm-facts`. | C06, C08, C10 |
| release | process **[changed]** | Reads `jvm-facts`. Creates a tag only after all suites pass. Publishes to Clojars and a mirror. Tag and artifacts signed with a key outside GitHub. | C04, C06, C08, C10 |

All other elements: as in `naive.md`.

## Connections (from uses to)

Removed:
- `cap-probe → clojure-asm`, `identity-backend → clojure-asm` (C02)

Added:
- `loader → compiler-shape`, `cap-probe → compiler-shape`, `field-cap-probe → compiler-shape`, `value-transform → compiler-shape`, `identity-backend → compiler-shape`, `compiler-shape → clj-compiler` (C01). The probe and the loader now meet in `compiler-shape`. This makes the hidden link of `coupling.md` explicit.
- `cap-probe → classfile-api`, `cap-probe → jvm-format`, `value-transform → jvm-format`, `jvm-format → valhalla-jvm` (C02, C09)
- `identity-backend → org.ow2.asm` (C02)
- `release → jvm-facts`, `test-matrix → jvm-facts`, `docs → jvm-facts`, `jvm-facts → jdk-archive` (C07, C10)
- `release → signing key`, `release → mirror` (C04, C08)

Unchanged: all other rows of `naive.md`. Two-way dependencies: none.

## Remaining failures

S101, S102, S106 (absurd; see `adaptation.md` section 7).
