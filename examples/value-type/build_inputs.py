#!/usr/bin/env python3
"""Write elements.tsv, stressors.tsv (with seeded split) and connections.tsv for run value-type-r1."""
import random

H = lambda skill: f"# run: value-type-r1 | date: 2026-11-06 | skill: {skill}\n"

ELEMENTS = [
 ("lib-author","library author","actor","Writes libraries with defvaluetype; must accept both representations."),
 ("app-author","application author/operator","actor","Selects JVM, flags, fallback policy; deploys."),
 ("maintainer","maintainer","actor","The one maintainer. Owns design, release, JVM tracking."),
 ("ai-agents","AI agents","actor","Write and review code, tests, docs under munera/ramora rules."),
 ("closed-record","closed-record","external","First user of defvaluetype* (record and closed record shapes)."),
 ("user-code","user code","actor","Programs that construct and use defined types and arrays; can depend on identity."),
 ("tooling","editor tooling","external","CIDER/nREPL; can call macroexpand outside compilation."),
 ("core-macro","value-type.core","component","defvaluetype, defvaluetype*, check-value-class: validate, select, expand."),
 ("array-api","value-type.array","component","make-array, into-array, array-info."),
 ("capability-report","value-type.capability","component","Public EDN report of four cached capability results."),
 ("runtime-policy","impl.runtime","component","Fallback policy (read once), warning flag, fallback guards."),
 ("cap-probe","impl.capability","component","Baseline-safe API checks, isolated value-class probe, cached result, value predicate."),
 ("field-cap-probe","impl.field-capability","component","Native non-nil field probe and cached result."),
 ("array-adapter","impl.array","component","Method handles to internal ValueClass; allocation/inspection capability."),
 ("fields","impl.fields","component","Field specifications: :non-nil, tag resolution, exact Class identity."),
 ("loader","impl.loader","component","Capture loader proxy of DynamicClassLoader; selects backend; AOT write; define and link."),
 ("value-transform","value backend","component","impl.value-backend, transform, class-file, field-storage, field-access: value-class bytes via java.lang.classfile."),
 ("identity-backend","impl.identity-backend","component","Identity output with typed storage and generated checks via clojure.asm."),
 ("clj-compiler","Clojure compiler 1.12.6","external","deftype*, Compiler/LOADER, NewInstanceExpr, writeClassFile, DynamicClassLoader cache."),
 ("clojure-asm","clojure.asm","external","ASM fork bundled in Clojure."),
 ("valhalla-jvm","Valhalla EA JVM","infrastructure","JEP 401 EA build 27-jep401ea3+1-1: class format rules, preview, verifier."),
 ("classfile-api","java.lang.classfile","external","JDK class-file API used for value output."),
 ("jdk-internal-value","jdk.internal.value","external","Internal ValueClass array allocation and NullRestricted annotation."),
 ("baseline-jvm","ordinary JVMs","infrastructure","Java 8+ without usable value classes; fallback target."),
 ("jvm-flags","JVM startup flags","infrastructure","--enable-preview, --add-exports, -Dvalue-type.fallback."),
 ("aot-output","consumer AOT output","artifact","Class files written at compile time; fixed representation."),
 ("expansion-transfer","transferred expansions","flow","Macroexpansion output evaluated in another loader, process or time."),
 ("source-jar","source-only JAR","artifact","build.clj; version 0.1.N from Git commit count."),
 ("release","release workflow","process","release.yml, deps-deploy, Clojars; not yet published."),
 ("test-matrix","test suites","artifact","Runtime, compatibility, cross-JVM, build tests in child JVMs; deftype compat corpus."),
 ("quality-ci","quality CI","process","GitHub Actions: cljfmt, clj-kondo, Vale, quickdoc API check, tooling tests."),
 ("docs","documentation","artifact","README, doc/usage, doc/API (generated), ramora designs, mementum."),
 ("benchmarks","benchmarks","artifact","dev/bench: method call, object size, typed array."),
]

# (category, stressor, affects)
S = [
 ("Market","Clojure core adds value-class support to deftype in a release.","lib-author,closed-record,core-macro,docs,user-code"),
 ("Market","A competing library gives value classes through gen-class and an annotation, and takes most users.","lib-author,docs,maintainer"),
 ("Market","closed-record removes its value-type dependency and emits value classes itself.","closed-record,core-macro"),
 ("Market","Users ask for the same defvaluetype source to work on ClojureScript and ClojureCLR.","lib-author,core-macro,fields,docs"),
 ("Market","Oracle stops Project Valhalla. No more EA builds are released.","valhalla-jvm,classfile-api,jdk-internal-value,value-transform,array-adapter,cap-probe,docs,test-matrix"),
 ("Customers and users","A user defines a type with 2000 fields.","core-macro,fields,value-transform,identity-backend,clj-compiler"),
 ("Customers and users","A popular library calls locking on value objects in a common code path.","user-code,valhalla-jvm,docs"),
 ("Customers and users","A large user AOT-compiles an application on Java 8 and deploys it on a Valhalla JVM with policy error.","aot-output,runtime-policy,app-author,valhalla-jvm"),
 ("Customers and users","A code generator evaluates 100000 defvaluetype forms at run time.","core-macro,loader,clj-compiler,cap-probe,runtime-policy"),
 ("Customers and users","Data scientists start to allocate arrays of one billion value objects.","array-api,array-adapter,jdk-internal-value,valhalla-jvm"),
 ("Customers and users","Java-only teams load AOT value types with Class.forName and no Clojure source.","aot-output,runtime-policy,user-code"),
 ("Organisation and people","The only maintainer stops work for one year.","maintainer,release,test-matrix,docs,ai-agents"),
 ("Organisation and people","The maintainer's employer forbids publication of code that depends on EA JVMs.","maintainer,release,source-jar"),
 ("Organisation and people","The AI model provider replaces the model. The new model ignores Simplified Technical English and Ramora rules.","ai-agents,docs,quality-ci"),
 ("Organisation and people","A second maintainer joins. They know the class-file format but not the Clojure compiler.","maintainer,loader,clj-compiler,docs"),
 ("Organisation and people","The closed-record author demands per-type fallback overrides and forks value-type.","closed-record,runtime-policy,core-macro"),
 ("Organisation and people","The maintainer decides to merge value-type into closed-record.","maintainer,closed-record,core-macro,release,docs"),
 ("Law and regulation","Oracle changes the EA build licence: no use in CI without an agreement.","valhalla-jvm,test-matrix,quality-ci,app-author"),
 ("Law and regulation","A court decides that shipping software that needs --add-exports of internal JDK packages breaks the JDK licence.","jdk-internal-value,jvm-flags,array-adapter,app-author"),
 ("Law and regulation","Clojars removes all EPL-licensed artifacts after a licence dispute.","release,source-jar,lib-author"),
 ("Law and regulation","A regulation requires signed, reproducible builds of all dependencies.","source-jar,release,quality-ci"),
 ("Money","GitHub Actions stops free minutes for public repositories.","quality-ci,test-matrix,release"),
 ("Money","Each new JVM row doubles the matrix cells. CI cost increases 10 times.","test-matrix,quality-ci,maintainer"),
 ("Money","A sponsor pays for support of five EA builds at the same time.","valhalla-jvm,cap-probe,value-transform,test-matrix,maintainer"),
 ("Money","The price of the AI agent service triples.","ai-agents,maintainer"),
 ("Suppliers and partners","Clojure 1.13 adds a hidden field to deftype classes and changes the constructor order.","clj-compiler,value-transform,identity-backend,loader,fields,test-matrix"),
 ("Suppliers and partners","Clojure removes the bundled clojure.asm package.","clojure-asm,identity-backend,cap-probe,clj-compiler"),
 ("Suppliers and partners","Clojure changes Compiler/LOADER so that let pushes a new loader.","clj-compiler,loader,core-macro,expansion-transfer"),
 ("Suppliers and partners","Clojars closes.","release,source-jar,lib-author"),
 ("Suppliers and partners","The Scry test runner is abandoned and fails on a new Clojure release.","test-matrix,quality-ci"),
 ("Suppliers and partners","The next EA build renames the methods of jdk.internal.value.ValueClass.","jdk-internal-value,array-adapter,field-cap-probe,capability-report"),
 ("Technology","A new EA build changes the ACC_STRICT_INIT value and the class version rule.","valhalla-jvm,classfile-api,value-transform,cap-probe,aot-output,test-matrix"),
 ("Technology","JEP 401 becomes final in JDK 28. The preview minor version and --enable-preview are not used.","valhalla-jvm,value-transform,cap-probe,jvm-flags,docs,aot-output,array-adapter"),
 ("Technology","The JVM replaces the NullRestricted annotation with a null-marker in field descriptors.","jdk-internal-value,value-transform,field-cap-probe,fields"),
 ("Technology","GraalVM native-image becomes the usual deployment target for Clojure applications.","aot-output,loader,clj-compiler,cap-probe,app-author"),
 ("Technology","CIDER starts to macroexpand each top-level form on each keystroke.","tooling,expansion-transfer,loader,core-macro"),
 ("Technology","The java.lang.classfile API changes the signatures of ClassFile.of and its options.","classfile-api,value-transform"),
 ("Technology","A JIT defect in an EA build gives wrong values from flattened arrays.","valhalla-jvm,array-api,user-code,benchmarks"),
 ("Data","A field tag names a class that a sibling plugin class loader defines.","fields,loader,clj-compiler,user-code"),
 ("Data","AOT class files from a different JDK feature release are on the class path.","aot-output,valhalla-jvm,runtime-policy"),
 ("Data","A production launcher sets value-type.fallback=wran.","jvm-flags,runtime-policy,app-author"),
 ("Data","A user persists serialized value objects and reads them on a fallback JVM.","user-code,baseline-jvm,valhalla-jvm,docs"),
 ("Data","Monitoring parses the capability report. A release adds and renames keys.","capability-report,app-author"),
 ("Security","An attacker publishes a malicious fork on Clojars with a similar coordinate.","release,lib-author,source-jar"),
 ("Security","A deployment platform forbids custom class loaders.","loader,clj-compiler,cap-probe,field-cap-probe,app-author"),
 ("Security","A CVE in clojure.asm forces an urgent Clojure update.","clojure-asm,clj-compiler,identity-backend,release"),
 ("Security","A library writes nil into a non-nil field through Unsafe. An attacker uses the resulting NullPointerException.","user-code,fields,docs"),
 ("Security","An attacker takes the maintainer's GitHub account and release.yml publishes a bad JAR.","release,quality-ci,maintainer"),
 ("Physical world","The maintainer's laptop is stolen. It has the only EA3 JDK, and EA3 is no longer available for download.","valhalla-jvm,test-matrix,maintainer,benchmarks"),
 ("Physical world","A power cut during release leaves partly uploaded artifacts.","release,source-jar"),
 ("Physical world","Servers become ARM-only. EA builds are available only for x86.","valhalla-jvm,test-matrix,app-author"),
 ("Society and politics","Sanctions block downloads of OpenJDK EA builds in the maintainer's country.","valhalla-jvm,test-matrix,maintainer"),
 ("Society and politics","The Clojure community boycotts libraries written by AI.","ai-agents,docs,lib-author,closed-record"),
 ("Time","Each EA build lasts three months. Four builds come each year.","valhalla-jvm,value-transform,cap-probe,test-matrix,aot-output,docs"),
 ("Time","After ten years, Java 8 is not available in CI images.","baseline-jvm,test-matrix,identity-backend"),
 ("Time","The matrix test duration increases to four hours.","test-matrix,maintainer,quality-ci"),
 ("Time","A shallow clone in CI gives version 0.1.1 and overwrites a published version.","source-jar,release"),
 ("Absurd","The JVM makes all value objects == to each other.","valhalla-jvm,user-code,array-api"),
 ("Absurd","Every field in every program is named __hash.","fields,core-macro,value-transform,closed-record"),
 ("Absurd","The JVM verifier rejects every class that has a constructor.","valhalla-jvm,baseline-jvm,value-transform,identity-backend"),
 ("Absurd","Java 8 gets value classes overnight through a back-port.","baseline-jvm,cap-probe,identity-backend,runtime-policy,test-matrix"),
 ("Absurd","A tool translates all documentation into Latin and the English source is lost.","docs,ai-agents,lib-author"),
 ("Absurd","Each thread of a program sees a different value of the fallback property.","runtime-policy,jvm-flags"),
 ("Absurd","The class-file format becomes JSON.","classfile-api,value-transform,identity-backend,clojure-asm,clj-compiler"), ("Society and politics","A government bans preview JVM features in public-sector software.","valhalla-jvm,jvm-flags,app-author,docs"),
 ("Society and politics","The media blames value objects for a bank outage. Managers forbid value-type.","app-author,lib-author,docs"),
 ("Physical world","A heat wave throttles the maintainer's machine. Benchmark noise exceeds 30%.","benchmarks,maintainer"),
 ("Physical world","A cosmic ray flips a bit in a cached capability result.","cap-probe,field-cap-probe,capability-report,runtime-policy"),
 ("Technology","nREPL evaluates forms on a thread with no Compiler/LOADER binding.","tooling,clj-compiler,loader,core-macro,expansion-transfer"),
 ("Data","A build tool caches macroexpansions on disk and replays them in a later JVM.","expansion-transfer,loader,core-macro,aot-output"),
 ("Customers and users","Operators call the capability report one million times per second.","capability-report,cap-probe,field-cap-probe,array-adapter"),
 ("Time","Users cite a two-year-old benchmark as a performance guarantee.","benchmarks,docs,user-code"),
 ("Absurd","Class.isValue disappears from every JVM on one day. Value classes still work.","cap-probe,core-macro,capability-report,valhalla-jvm"),
]

CONN = """lib-author core-macro
lib-author array-api
lib-author docs
app-author jvm-flags
app-author capability-report
app-author array-api
app-author docs
app-author aot-output
closed-record core-macro
user-code core-macro
user-code array-api
user-code valhalla-jvm
user-code baseline-jvm
core-macro runtime-policy
core-macro cap-probe
core-macro field-cap-probe
core-macro fields
core-macro loader
core-macro clj-compiler
capability-report cap-probe
capability-report field-cap-probe
capability-report array-adapter
array-api array-adapter
array-adapter cap-probe
array-adapter jdk-internal-value
array-adapter jvm-flags
runtime-policy jvm-flags
cap-probe clojure-asm
cap-probe clj-compiler
cap-probe valhalla-jvm
cap-probe baseline-jvm
field-cap-probe cap-probe
field-cap-probe jdk-internal-value
field-cap-probe clj-compiler
fields cap-probe
fields clj-compiler
loader clj-compiler
loader value-transform
loader identity-backend
loader aot-output
value-transform fields
value-transform classfile-api
value-transform valhalla-jvm
value-transform jdk-internal-value
identity-backend fields
identity-backend clojure-asm
identity-backend baseline-jvm
aot-output valhalla-jvm
aot-output baseline-jvm
aot-output runtime-policy
expansion-transfer core-macro
expansion-transfer loader
tooling expansion-transfer
tooling clj-compiler
release source-jar
release quality-ci
maintainer release
maintainer test-matrix
maintainer quality-ci
maintainer docs
maintainer benchmarks
maintainer ai-agents
ai-agents docs
ai-agents test-matrix
ai-agents quality-ci
test-matrix valhalla-jvm
test-matrix baseline-jvm
test-matrix jvm-flags
test-matrix core-macro
test-matrix array-api
test-matrix aot-output
test-matrix clj-compiler
quality-ci docs
quality-ci core-macro
benchmarks valhalla-jvm
benchmarks array-api
benchmarks core-macro"""

SEED = 20261106
ids = [f"S{i:02d}" for i in range(1, len(S) + 1)]
n_test = round(len(S) * 0.25)
test = set(random.Random(SEED).sample(ids, n_test))
eids = {e[0] for e in ELEMENTS}
for c, _, a in S:
    for e in a.split(','):
        assert e in eids, e
with open('elements.tsv', 'w') as f:
    f.write(H('generate-stressors'))
    f.write("id\tname\tkind\tdescription\n")
    for e in ELEMENTS:
        f.write("\t".join(e) + "\n")
with open('stressors.tsv', 'w') as f:
    f.write(H('generate-stressors'))
    f.write(f"# split: random.Random({SEED}).sample, {n_test}/{len(S)} test (25%), date 2026-11-06, before adaptation\n")
    f.write("id\tcategory\tstressor\taffects\tset\n")
    for sid, (c, s, a) in zip(ids, S):
        f.write(f"{sid}\t{c}\t{s}\t{a}\t{'test' if sid in test else 'training'}\n")
with open('connections.tsv', 'w') as f:
    f.write(H('find-hidden-coupling'))
    f.write("from\tto\n")
    for line in CONN.splitlines():
        a, b = line.split()
        assert a in eids and b in eids, line
        f.write(f"{a}\t{b}\n")
print(len(S), "stressors;", n_test, "test:", sorted(test))
