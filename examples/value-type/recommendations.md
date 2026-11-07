# Recommended changes for value-type

Source: runs [value-type-r1](README.md) (with pass 3) and [value-type-r2](../value-type-r2/README.md), value-type commit `5073893f`. Decisions by the user, 2026-11-06.

Both evaluations give Ri = 0.00 with a maximum of about 0.10. The changes come from training stressors. No test set measured a gain.

## Decided

| # | Change | Decision | Runs |
|---|---|---|---|
| 1 | **Probes on `java.lang.classfile`.** `impl.capability/probe-bytes` (used by the value probe and the field probe) builds classes with `java.lang.classfile`. The probes run only after the API is found. | Probes only. `impl.identity-backend` keeps `clojure.asm`: it must run on Java 8–23, and `java.lang.classfile` is final only in JDK 24. No `org.ow2.asm` dependency. | r1 C02, r2 C02 |
| 2 | **JVM format table, fail-open.** One namespace owns the JEP 401 flag values, the version rule and the constructor order rule. The default row is the current rule (`latestMajorVersion`, preview minor version, current flags). Other rows record only known differences, keyed by feature release or build. A build with no row uses the default row. The probe defines and checks a real value class, so a wrong row fails in the probe, as it does today. | Fail-open. No `:unknown-jvm-format` reason. | r1 C03, r2 C09 |
| 3 | **Fallback policy at the first decision.** Read `value-type.fallback` at the first fallback decision, not at namespace load. The value is then fixed for the runtime. `value-type.capability/report` adds the policy in effect. | Yes. The first read fixes the policy, from a fallback decision or from a report call. An invalid value throws at the first read, not at load. The report makes it visible on a capable JVM. | r2 C05 (replaced) |
| 4 | **One file of supported-JVM facts:** JVMs, build IDs, URLs, SHA-256. `release.yml`, tests and documents read it or link to it. | Yes. | r1 C05, r2 C10 |
| 5 | **Compiler boundary as structure only.** One namespace owns the model of compiler output and the class definition through `DynamicClassLoader` (probes and loader). Keep the current clear error ("Fix: use Clojure 1.12"). Do not convert it to fallback. | Yes. | r1 C01, r2 C01 |
| 6 | **Install tested releases:** README installs a release tag or the Clojars version, not `master`. | Yes. | r2 C06 |
| 7 | **Receiving expansion for all definitions.** Removes the `installed=true` literal of replayed expansions. | Yes. | r1 C08 |
| 8 | **Value-class switch** `-Dvalue-type.value-classes=off`: value-class capability unavailable (`:disabled`), fallback by policy; arrays fail clearly. | Yes. | r1 C09 |
| 9 | **Forced-JIT test row** before an EA build is claimed. | Yes. | r1 C11 |
| 10 | **Disassembly snapshots** of the compatibility corpus. | Yes. | r2 C03 |
| 11 | **Tiered test matrix:** full matrix on the primary pair, smoke rows for other JVMs. | Yes. | r1 C04 |
| 12 | **Semantic self-check.** Object checks (42, 43, 42 with the probe class; own values; 42 ≠ 43 and 42 = 42 by `identical?`), nil check, array round trip in `impl.array` discovery, and a load-time check of AOT value output. A failure gives `:failed-self-check`, then fallback by policy (values) or a clear failure (arrays). Cost: see below. | Yes, all parts. Measure the AOT startup cost when the AOT check is built. | r1 C10, r2 C11 |
| 13 | **Field probe classification.** `impl.field-capability`: when the JVM ignores `NullRestricted`, report unavailable, not "accepted null". | Yes. | r2 S118 |
| 14 | **Value probe classification.** `impl.capability`: when the probe class is defined but is not a value class (for example a flag that switches value classes off), report unavailable, not an invariant error. | Yes. | r2 S051 |
| — | **Release signature outside GitHub.** | No. | r1 C06, r2 C08 |
| — | **Archive tested JDKs.** | No. The project follows EA changes: it moves to each new EA build. | r1 C07, r2 C07 |
| — | **Two channels** (Clojars and a mirror). | No. | r2 C04 |

`silent` stays silent. No change prints a message under `silent`.

## Cost of the semantic self-check (decision 12)

A JVM value-semantics defect passes the probe silently today. Parts:

| Part | Run-time cost | Code cost |
|---|---|---|
| Object checks: 42, 43, 42 with the probe class; own values; 42 ≠ 43 and 42 = 42 by `identical?`. | Once per runtime, inside the existing `delay`. Three reflective constructor calls. No new class. | About 10 lines. The failure path is testable without mocks: an identity class fails "equal objects are `identical?`". |
| nil check (r2 S099). | Negligible. | 1–2 lines. |
| Array round trip in `impl.array` discovery. | Once per runtime, only where arrays are available. | About 10 lines and a test row. |
| Load-time check of AOT value output. | Each AOT application runs the probe at startup (loads `java.lang.classfile`, defines one class). Probably tens of milliseconds. Measure first. | Small with decision 7. AOT tests. |

## Not addressed

- r2 S073: a false `value-type.impl` namespace earlier on the class path.
- r1 S38: JIT-only array defects that no test exercises.
