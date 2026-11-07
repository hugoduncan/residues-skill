# run: value-type-r2 | date: 2026-11-06 | skill: adapt-design

# Criteria

Status: CONFIRMED. Copied unchanged from run value-type-r1 (same design, same user confirmation).
Source: README, `ramora/defvaluetype-design.md`, non-nil field, deftype* and array designs (purpose and priorities).

## Essential functions

| ID | Function |
|---|---|
| F1 | A `defvaluetype` or `defvaluetype*` form defines a class with `deftype`/`deftype*` syntax and behaviour. It is a value class when the JVM supports it, else an identity class as the policy permits. |
| F2 | The application fallback policy (`silent`, `warn`, `error`) controls the representation. A strict failure is never skipped. |
| F3 | Enabled `:non-nil` fields reject nil and wrong types on all supported constructor paths, in both representations. |
| F4 | The public namespaces load on JVMs without value-class support and without optional JDK APIs. |
| F5 | On a supported JVM, `value-type.array` gives native null-restricted atomic arrays. On other JVMs it fails clearly. |
| F6 | The capability report gives true results for the running JVM. |
| F7 | A consumer can get the library, and the maintainer can verify it on the JVMs that it claims to support. |

## Survive

The design survives a stressor if, after the stressor, F1–F7 still hold, or return with acceptable effort.

- A clear, early failure that names the cause and the fix counts as "keeps the function" for an unsupported environment (F1 identity fallback, F5 clear failure).
- Silent wrong behaviour does not survive: wrong representation, a skipped policy, a field that accepts nil, a false capability report.
- Loss of value-class output on a JVM that the design does not claim to support is acceptable. The project is experimental and has no stable API.

## Acceptable effort

- The maintainer alone does the change, in at most a few days.
- The change stays inside one boundary: at most two namespaces plus their test rows, or documentation or configuration only.
- No change to the public API syntax. Breaking changes are allowed (no backward compatibility, AGENTS.md), but must be documented.
- The change does not need a new external supplier, a JVM agent, or Java source.

## Confirmation

Confirmed by: user (Hugo Duncan), unchanged from proposal
Date: 2026-11-06
