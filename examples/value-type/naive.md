# run: value-type-r1 | date: 2026-11-06 | skill: adapt-design

# Naive design (control). Do not change.

Source: value-type commit `5073893f`, 2026-11-06. Copy of `design.md` below, plus elements.tsv and connections.tsv of this run as written before adaptation.

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

## Elements

```tsv
id	name	kind	description
lib-author	library author	actor	Writes libraries with defvaluetype; must accept both representations.
app-author	application author/operator	actor	Selects JVM, flags, fallback policy; deploys.
maintainer	maintainer	actor	The one maintainer. Owns design, release, JVM tracking.
ai-agents	AI agents	actor	Write and review code, tests, docs under munera/ramora rules.
closed-record	closed-record	external	First user of defvaluetype* (record and closed record shapes).
user-code	user code	actor	Programs that construct and use defined types and arrays; can depend on identity.
tooling	editor tooling	external	CIDER/nREPL; can call macroexpand outside compilation.
core-macro	value-type.core	component	defvaluetype, defvaluetype*, check-value-class: validate, select, expand.
array-api	value-type.array	component	make-array, into-array, array-info.
capability-report	value-type.capability	component	Public EDN report of four cached capability results.
runtime-policy	impl.runtime	component	Fallback policy (read once), warning flag, fallback guards.
cap-probe	impl.capability	component	Baseline-safe API checks, isolated value-class probe, cached result, value predicate.
field-cap-probe	impl.field-capability	component	Native non-nil field probe and cached result.
array-adapter	impl.array	component	Method handles to internal ValueClass; allocation/inspection capability.
fields	impl.fields	component	Field specifications: :non-nil, tag resolution, exact Class identity.
loader	impl.loader	component	Capture loader proxy of DynamicClassLoader; selects backend; AOT write; define and link.
value-transform	value backend	component	impl.value-backend, transform, class-file, field-storage, field-access: value-class bytes via java.lang.classfile.
identity-backend	impl.identity-backend	component	Identity output with typed storage and generated checks via clojure.asm.
clj-compiler	Clojure compiler 1.12.6	external	deftype*, Compiler/LOADER, NewInstanceExpr, writeClassFile, DynamicClassLoader cache.
clojure-asm	clojure.asm	external	ASM fork bundled in Clojure.
valhalla-jvm	Valhalla EA JVM	infrastructure	JEP 401 EA build 27-jep401ea3+1-1: class format rules, preview, verifier.
classfile-api	java.lang.classfile	external	JDK class-file API used for value output.
jdk-internal-value	jdk.internal.value	external	Internal ValueClass array allocation and NullRestricted annotation.
baseline-jvm	ordinary JVMs	infrastructure	Java 8+ without usable value classes; fallback target.
jvm-flags	JVM startup flags	infrastructure	--enable-preview, --add-exports, -Dvalue-type.fallback.
aot-output	consumer AOT output	artifact	Class files written at compile time; fixed representation.
expansion-transfer	transferred expansions	flow	Macroexpansion output evaluated in another loader, process or time.
source-jar	source-only JAR	artifact	build.clj; version 0.1.N from Git commit count.
release	release workflow	process	release.yml, deps-deploy, Clojars; not yet published.
test-matrix	test suites	artifact	Runtime, compatibility, cross-JVM, build tests in child JVMs; deftype compat corpus.
quality-ci	quality CI	process	GitHub Actions: cljfmt, clj-kondo, Vale, quickdoc API check, tooling tests.
docs	documentation	artifact	README, doc/usage, doc/API (generated), ramora designs, mementum.
benchmarks	benchmarks	artifact	dev/bench: method call, object size, typed array.
```

## Connections (from uses to)

```tsv
from	to
lib-author	core-macro
lib-author	array-api
lib-author	docs
app-author	jvm-flags
app-author	capability-report
app-author	array-api
app-author	docs
app-author	aot-output
closed-record	core-macro
user-code	core-macro
user-code	array-api
user-code	valhalla-jvm
user-code	baseline-jvm
core-macro	runtime-policy
core-macro	cap-probe
core-macro	field-cap-probe
core-macro	fields
core-macro	loader
core-macro	clj-compiler
capability-report	cap-probe
capability-report	field-cap-probe
capability-report	array-adapter
array-api	array-adapter
array-adapter	cap-probe
array-adapter	jdk-internal-value
array-adapter	jvm-flags
runtime-policy	jvm-flags
cap-probe	clojure-asm
cap-probe	clj-compiler
cap-probe	valhalla-jvm
cap-probe	baseline-jvm
field-cap-probe	cap-probe
field-cap-probe	jdk-internal-value
field-cap-probe	clj-compiler
fields	cap-probe
fields	clj-compiler
loader	clj-compiler
loader	value-transform
loader	identity-backend
loader	aot-output
value-transform	fields
value-transform	classfile-api
value-transform	valhalla-jvm
value-transform	jdk-internal-value
identity-backend	fields
identity-backend	clojure-asm
identity-backend	baseline-jvm
aot-output	valhalla-jvm
aot-output	baseline-jvm
aot-output	runtime-policy
expansion-transfer	core-macro
expansion-transfer	loader
tooling	expansion-transfer
tooling	clj-compiler
release	source-jar
release	quality-ci
maintainer	release
maintainer	test-matrix
maintainer	quality-ci
maintainer	docs
maintainer	benchmarks
maintainer	ai-agents
ai-agents	docs
ai-agents	test-matrix
ai-agents	quality-ci
test-matrix	valhalla-jvm
test-matrix	baseline-jvm
test-matrix	jvm-flags
test-matrix	core-macro
test-matrix	array-api
test-matrix	aot-output
test-matrix	clj-compiler
quality-ci	docs
quality-ci	core-macro
benchmarks	valhalla-jvm
benchmarks	array-api
benchmarks	core-macro
```
