# run: value-type-r1 | date: 2026-11-06 | skill: generate-stressors

# Design: value-type

Source: `~/projects/hugoduncan/value-type/value-type-master`, commit `5073893f` (2026-11-06).
Documents read: `README.md`, `mementum/state.md`, `ramora/defvaluetype-design.md` and
`defvaluetype-design/{context,decisions,embodiment,embodiment/runtime,embodiment/artifacts,fallback,risks-and-evolution}.md`,
`defvaluetype-design/decisions/{compiler-and-capture,transform-and-aot}.md`,
`ramora/{non-nil-field-design,deftype-star-design,value-type-array-design}.md`,
`deftype-star-design/purpose.md`, the `ns` forms of `src/`, `deps.edn`, `bb.edn`.

## Scope and level of detail

The design is approximately 30,000 words. Scope: component level. Elements are actors,
public namespaces, implementation namespaces (helpers of the value transform
merged into one element), external systems, and delivery artifacts (AOT output,
JAR, release, tests, CI, documentation). Method-level detail and individual
decisions are out of scope. Open task 022 (closed record shape) is in scope as part of
`defvaluetype*` (element `core-macro`).

## Summary

value-type is an experimental Clojure library. `defvaluetype` has `deftype`
syntax and gives a JEP 401 value class on a supported Valhalla early-access JVM.
`defvaluetype*` takes `deftype*` arguments (plain, record and closed record shapes);
closed-record is its first user.

```text
defvaluetype → validate fields → capability probe + application policy
  supported   → install capture loader (Compiler/LOADER) → deftype
                → transform bytes (java.lang.classfile) → write .class (AOT)
                → define and link → check value class
  unavailable → policy silent: deftype | warn: warn once, deftype | error: Error
```

- Application policy: JVM property `value-type.fallback` (`silent`, `warn`, `error`), read once.
- `:non-nil` fields: native enforcement (internal `NullRestricted`) on value classes when available;
  else generated constructor checks. The identity backend uses bundled `clojure.asm`, so it loads on Java 8.
- Capability probes (value class, native field, array allocation, array inspection) are cached
  in their namespaces; `value-type.capability/report` returns them as EDN.
- `value-type.array`: null-restricted atomic arrays through internal
  `jdk.internal.value.ValueClass`. Needs `--enable-preview` and `--add-exports`. No fallback.
- AOT fixes representation. Value-class AOT output is tied to one JDK feature release.
  Fallback AOT output carries a policy guard.
- Delivery: source-only JAR (version = Git commit count), release to Clojars through deps-deploy
  (not yet published), test suites in child JVMs (Java 8, EA3 preview off/on), quality CI
  (format, lint, Vale prose, generated API docs). One maintainer; AI agents write code and docs.
