# Recommended changes for value-type

Source: runs [value-type-r1](README.md) (with pass 3) and [value-type-r2](../value-type-r2/README.md), value-type commit `5073893f`. Decisions by the user, 2026-11-06.

Both evaluations give Ri = 0.00 with a maximum of about 0.10. The changes come from training stressors. No test set measured a gain.

## Decided

| # | Change | Decision | Runs |
|---|---|---|---|
| 1 | **Probes on `java.lang.classfile`.** `impl.capability/probe-bytes` (used by the value probe and the field probe) builds classes with `java.lang.classfile`. The probes run only after the API is found. | Probes only. `impl.identity-backend` keeps `clojure.asm`: it must run on Java 8–23, and `java.lang.classfile` is final only in JDK 24. No `org.ow2.asm` dependency. | r1 C02, r2 C02 |
| 2 | **JVM format table, fail-open.** One namespace owns the JEP 401 flag values, the version rule and the constructor order rule. The default row is the current rule (`latestMajorVersion`, preview minor version, current flags). Other rows record only known differences, keyed by feature release or build. A build with no row uses the default row. The probe defines and checks a real value class, so a wrong row fails in the probe, as it does today. | Fail-open. No `:unknown-jvm-format` reason. | r1 C03, r2 C09 |
| 3 | **Fallback policy at the first decision.** Read `value-type.fallback` at the first fallback decision, not at namespace load. The value is then fixed for the runtime. `value-type.capability/report` adds the policy in effect. | Decided. Open details: does a report call fix the policy (recommended: yes, the first read fixes it)? An invalid value is found at the first read, not at load. The report makes it visible on a capable JVM. | r2 C05 (replaced) |
| — | **Release signature outside GitHub.** | Dropped. | r1 C06, r2 C08 |

`silent` stays silent. No change prints a message under `silent`.

## Recommended, not decided

| Change | Why | Runs |
|---|---|---|
| **Semantic self-check.** The probe checks that two objects keep their own values, that different objects are not `==`, and that equal objects are `==`. A failure gives `:failed-self-check`, then fallback by policy. Optional: also compare with nil (r2 S099). | A JVM value-semantics defect passes the probe silently. | r1 C10, r2 C11 |
| **One file of supported-JVM facts:** JVMs, build IDs, URLs, SHA-256. `release.yml`, tests and documents read it or link to it. | 405 mentions of EA3 in 204 files. | r1 C05, r2 C10 |
| **Archive tested JDKs:** private, off-site, with checksums. | EA builds disappear from the download site. | r1 C07, r2 C07 |
| **Compiler boundary as structure only.** One namespace owns the model of compiler output and the class definition through `DynamicClassLoader` (probes and loader). Keep the current clear error ("Fix: use Clojure 1.12"). Do not convert it to fallback. | Fewer places change for a new Clojure version. Shows the hidden probe–loader link (r2). | r1 C01, r2 C01 |
| **Install tested releases:** README installs a release tag or the Clojars version, not `master`. | CI on push runs no runtime or fallback suite. | r2 C06 |
| **Two channels:** Clojars and a mirror. | GitHub is the only channel. | r2 C04 |
| **Receiving expansion for all definitions.** | A replayed expansion has a misleading `installed=true` literal. | r1 C08 |
| **Value-class switch** `-Dvalue-type.value-classes=off`. | No return after a JVM defect is found. | r1 C09 |
| **Forced-JIT test row** before an EA build is claimed. | Some defects show only in compiled code. | r1 C11 |
| **Disassembly snapshots** of the compatibility corpus. | A review of the source diff does not show a change of emitted bytes. | r2 C03 |
| **Tiered test matrix.** | Matrix cost grows with each JVM row. | r1 C04 |

## Small fixes

- `impl.field-capability`: when the JVM ignores `NullRestricted`, report unavailable, not "accepted null" (r2 S118).
- `impl.capability`: when the probe class is defined but is not a value class (for example a flag that switches value classes off), report unavailable, not an invariant error (r2 S051).

## Not addressed

- r2 S073: a false `value-type.impl` namespace earlier on the class path.
- r1 S38: JIT-only array defects that no test exercises.
