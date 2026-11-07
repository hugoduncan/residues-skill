#!/usr/bin/env python3
"""Write elements.tsv, stressors.tsv (seeded split after coverage) and connections.tsv for run value-type-r2.

The design, scope, elements and connections are the same as run value-type-r1
(../value-type). The stressors are new. Usage:
  python3 build_inputs.py --coverage   # report coverage, write nothing
  python3 build_inputs.py              # write the run record inputs
"""
import collections, csv, random, sys

RUN, DATE = "value-type-r2", "2026-11-06"
H = lambda skill: f"# run: {RUN} | date: {DATE} | skill: {skill}\n"

def read_tsv(path):
    with open(path) as f:
        return [r for r in csv.reader((l for l in f if not l.startswith('#')), delimiter='\t')][1:]

ELEMENTS = read_tsv('../value-type/elements.tsv')
CONN = read_tsv('../value-type/connections.tsv')

# Step 2-5: generated stressors (category, stressor, affects).
S_INITIAL = [
 # Market
 ("Market","Kotlin value classes become the usual form for JVM library APIs. Clojure users ask to implement and consume them from defvaluetype.","user-code,core-macro,fields,docs"),
 ("Market","A large company offers to buy value-type and close the source.","maintainer,release,source-jar,docs"),
 ("Market","Nobody downloads value-type for two years.","maintainer,release,docs,ai-agents"),
 ("Market","A popular data library adopts value-type. Users increase from 10 to 100000 in one month.","lib-author,user-code,docs,release,maintainer"),
 ("Market","Value classes become standard on every JVM. Nobody needs identity fallback.","baseline-jvm,identity-backend,runtime-policy,docs,test-matrix"),
 ("Market","Clojure contrib publishes a supported alternative to value-type with a different syntax.","lib-author,closed-record,docs"),
 ("Market","closed-record becomes ten times more popular than value-type. Its users report all defects against value-type.","closed-record,maintainer,docs"),
 ("Market","An IDE vendor sells a plugin that reads value-type private namespaces.","tooling,cap-probe,loader,value-transform"),
 # Customers and users
 ("Customers and users","A user defines 50000 value types in one namespace.","core-macro,loader,clj-compiler,cap-probe,aot-output"),
 ("Customers and users","A user evaluates defvaluetype inside a binding that changes *compile-files*.","core-macro,loader,aot-output,clj-compiler"),
 ("Customers and users","A user sends serialized value objects over RMI to a JVM with no value classes.","user-code,baseline-jvm,valhalla-jvm"),
 ("Customers and users","Users put value objects as keys in a WeakHashMap.","user-code,valhalla-jvm,docs"),
 ("Customers and users","A user redefines one value type 1000 times at the REPL, with different fields each time.","core-macro,loader,clj-compiler,tooling,user-code"),
 ("Customers and users","Users call array-info on arrays that another library made in a different class loader.","array-api,array-adapter,user-code"),
 ("Customers and users","An operator sets policy error in production. A dependency contains fallback AOT output.","runtime-policy,aot-output,app-author,jvm-flags"),
 ("Customers and users","A user extends a protocol to a value type from a namespace that loads before the type.","user-code,core-macro,clj-compiler,loader"),
 ("Customers and users","A university course uses value-type on Java 21 without preview.","user-code,baseline-jvm,runtime-policy,docs"),
 # Organisation and people
 ("Organisation and people","The maintainer gives value-type to clj-commons. Each review takes months.","maintainer,release,quality-ci,docs"),
 ("Organisation and people","AI agents open 500 pull requests in one week.","ai-agents,quality-ci,test-matrix,maintainer"),
 ("Organisation and people","A contributor rewrites the value backend in Java.","value-transform,source-jar,release,quality-ci"),
 ("Organisation and people","The maintainer forgets the design reasons. The Ramora documents are out of date.","docs,maintainer,ai-agents"),
 ("Organisation and people","The Valhalla team hires the maintainer and forbids public work.","maintainer,valhalla-jvm,docs"),
 ("Organisation and people","A reviewer with commit access merges a change that disables the error policy.","runtime-policy,maintainer,quality-ci,release"),
 ("Organisation and people","The maintainer's new employer forbids AI-written code.","ai-agents,maintainer,docs,test-matrix"),
 ("Organisation and people","The closed-record maintainer leaves. closed-record is not maintained.","closed-record,core-macro,test-matrix"),
 # Law and regulation
 ("Law and regulation","A law requires a five-year security-update promise from maintainers who receive money.","maintainer,release,docs"),
 ("Law and regulation","A law requires an SBOM for each artifact on Clojars.","release,source-jar,quality-ci"),
 ("Law and regulation","A court in one country decides that EPL 2.0 is not valid there.","source-jar,release,lib-author"),
 ("Law and regulation","Export control classifies JVM preview features as dual-use technology.","valhalla-jvm,jvm-flags,app-author"),
 ("Law and regulation","A court decides that AI-written code has no copyright. The licence of most of the code is not clear.","ai-agents,source-jar,release,docs"),
 ("Law and regulation","A regulator forbids preview JVM features and internal JDK packages in safety-critical software.","jvm-flags,jdk-internal-value,valhalla-jvm,app-author,array-api"),
 ("Law and regulation","Oracle registers 'value class' as a trademark and forbids it in third-party documentation.","docs,capability-report,core-macro"),
 ("Law and regulation","An audit requires a log entry for each run-time capability decision.","cap-probe,runtime-policy,capability-report,app-author"),
 # Money
 ("Money","Clojars charges for each download.","release,source-jar,lib-author"),
 ("Money","The maintainer's machine fails. There is no money for a machine with enough memory for the matrix.","maintainer,test-matrix,benchmarks"),
 ("Money","A sponsor pays only for work on arrays.","array-api,array-adapter,maintainer"),
 ("Money","Memory prices fall 100 times. Memory savings from value classes are worth almost nothing.","user-code,benchmarks,docs"),
 ("Money","GitHub charges for Actions caches and release storage.","quality-ci,release,test-matrix"),
 ("Money","A bounty pays for support of Clojure 1.10 and 1.11.","clj-compiler,loader,value-transform,identity-backend,test-matrix"),
 ("Money","The AI agent service becomes free, but gives one answer each hour.","ai-agents,maintainer"),
 ("Money","A company pays to keep EA3 supported for five years.","valhalla-jvm,test-matrix,maintainer,cap-probe"),
 # Suppliers and partners
 ("Suppliers and partners","Oracle stops EA builds for macOS.","valhalla-jvm,maintainer,test-matrix"),
 ("Suppliers and partners","deps-deploy is abandoned and stops working with Clojars.","release,source-jar"),
 ("Suppliers and partners","A clj-kondo release stops reading the defvaluetype lint hooks.","quality-ci,tooling,core-macro"),
 ("Suppliers and partners","Clojure 1.13 replaces NewInstanceExpr with a new deftype compiler.","clj-compiler,loader,value-transform,identity-backend,fields"),
 ("Suppliers and partners","Clojure removes the class cache of DynamicClassLoader.","clj-compiler,loader,cap-probe"),
 ("Suppliers and partners","Vale changes its rules. All documents fail the prose check.","quality-ci,docs"),
 ("Suppliers and partners","Adoptium publishes Valhalla builds with flags that are different from the Oracle builds.","valhalla-jvm,jvm-flags,cap-probe,test-matrix"),
 ("Suppliers and partners","quickdoc is abandoned.","quality-ci,docs"),
 ("Suppliers and partners","GitHub is not available for one month.","quality-ci,release,maintainer,source-jar"),
 # Technology
 ("Technology","The JVM adds a run-time flag that switches value classes off (-XX:-ValueClasses).","valhalla-jvm,cap-probe,jvm-flags,aot-output"),
 ("Technology","A new EA build removes ValueClass.newNullRestrictedAtomicArray.","jdk-internal-value,array-adapter,array-api"),
 ("Technology","The JVM changes == for value objects with float fields to compare bits.","valhalla-jvm,user-code,fields"),
 ("Technology","Clojure compiles protocol calls to invokedynamic.","clj-compiler,value-transform,identity-backend"),
 ("Technology","A new EA build limits value classes to 64 fields.","valhalla-jvm,value-transform,fields,core-macro"),
 ("Technology","An application runs on the module path. value-type has no module-info.","jvm-flags,array-adapter,jdk-internal-value,source-jar,app-author"),
 ("Technology","Project Leyden AOT caches store loaded classes and replay them at startup.","aot-output,loader,cap-probe,valhalla-jvm"),
 ("Technology","A new EA build changes the class-file major version inside one feature release.","valhalla-jvm,cap-probe,value-transform,aot-output"),
 ("Technology","A GC in a new EA build moves flattened fields. Unsafe offsets become wrong.","valhalla-jvm,user-code,benchmarks"),
 ("Technology","Babashka supports defvaluetype through SCI.","core-macro,tooling,cap-probe,baseline-jvm"),
 # Data
 ("Data","A field tag names a class that is renamed between AOT compilation and run time.","fields,aot-output,user-code"),
 ("Data","A user stores value objects in Datomic and reads them after a change of representation.","user-code,valhalla-jvm,baseline-jvm,docs"),
 ("Data","An application uses the printed form of value objects as a cache key. The form changes with the representation.","user-code,core-macro,docs"),
 ("Data","The documented download SHA of the EA build is wrong and matches a different build.","valhalla-jvm,test-matrix,maintainer,docs"),
 ("Data","An editor hot-swaps classes. The capability report shows the result from before the swap.","capability-report,cap-probe,tooling"),
 ("Data","Deserialization with readObject puts nil into a :non-nil field.","fields,user-code,identity-backend,value-transform"),
 ("Data","Somebody rewrites the Git history. The commit count, and so the version, goes down.","source-jar,release"),
 ("Data","A fixture file of the deftype compatibility corpus is corrupted.","test-matrix,quality-ci"),
 # Security
 ("Security","An attacker uses an AI agent to submit a pull request that adds a hidden step to the transform.","ai-agents,value-transform,quality-ci,maintainer"),
 ("Security","An attacker replaces closed-record on Clojars with a version that pins an old value-type.","closed-record,release,lib-author"),
 ("Security","A new JDK access policy forbids defineClass for classes that are not hidden classes.","loader,cap-probe,valhalla-jvm,clj-compiler"),
 ("Security","Attackers make many value objects with the same hash to slow down maps.","user-code,valhalla-jvm,fields"),
 ("Security","A dependency-confusion attack puts a false value-type.impl namespace earlier on the class path.","source-jar,core-macro,app-author"),
 ("Security","The GitHub Actions runner image is compromised.","quality-ci,release,test-matrix"),
 ("Security","Secrets in value-object fields appear in heap dumps of flat arrays, without their objects.","user-code,array-api,docs"),
 ("Security","The EA JDK download site serves a trojan build.","valhalla-jvm,maintainer,test-matrix"),
 # Physical world
 ("Physical world","A flood destroys the maintainer's machines and the backups in the same house.","maintainer,test-matrix,docs,release"),
 ("Physical world","A pandemic stops the maintainer's work for six months.","maintainer,ai-agents,release"),
 ("Physical world","An internet outage cuts off the maintainer for two weeks during a JVM change.","maintainer,valhalla-jvm,quality-ci"),
 ("Physical world","A solar storm corrupts a Clojure JAR in the CI cache.","quality-ci,clj-compiler,test-matrix"),
 ("Physical world","Embedded users run value-type on devices with 64 MB of memory.","user-code,cap-probe,baseline-jvm,valhalla-jvm"),
 ("Physical world","Data centres in one region stop. The nearest Clojars mirror is not available.","release,source-jar,lib-author"),
 ("Physical world","The maintainer moves to a time zone 12 hours from all other contributors.","maintainer,ai-agents"),
 # Society and politics
 ("Society and politics","A war blocks the maintainer's access to GitHub and to Oracle sites.","maintainer,quality-ci,release,valhalla-jvm"),
 ("Society and politics","Open-source developers strike against AI training on their code.","ai-agents,docs,maintainer"),
 ("Society and politics","The Clojure community splits into two forks of Clojure.","clj-compiler,lib-author,test-matrix,loader"),
 ("Society and politics","A public campaign calls preview features unsafe. Libraries remove value-type.","closed-record,lib-author,docs,app-author"),
 ("Society and politics","A government requires all software to run on a national JVM fork without Valhalla.","baseline-jvm,app-author,runtime-policy"),
 ("Society and politics","Social media spreads a false claim that value-type corrupts data.","docs,maintainer,lib-author"),
 ("Society and politics","A country blocks Clojars.","release,source-jar,app-author"),
 # Time
 ("Time","Valhalla needs twenty more years to become final.","valhalla-jvm,maintainer,docs,test-matrix"),
 ("Time","JEP 401 becomes final next month, two years early.","valhalla-jvm,cap-probe,value-transform,docs,jvm-flags"),
 ("Time","An application sets the fallback property with System/setProperty after value-type has loaded.","runtime-policy,jvm-flags,app-author"),
 ("Time","A server runs for five years with no restart. The JVM files are updated below it.","cap-probe,valhalla-jvm,app-author"),
 ("Time","The release workflow runs on two commits at the same time.","release,source-jar,quality-ci"),
 ("Time","A clock change makes build timestamps go backwards.","source-jar,release,aot-output"),
 ("Time","Clojure releases a new minor version each month.","clj-compiler,loader,value-transform,identity-backend,test-matrix"),
 ("Time","An AOT-compiled application stays in production ten years after its JDK release ends.","aot-output,valhalla-jvm,app-author"),
 # Absurd
 ("Absurd","Every value object becomes == to nil.","valhalla-jvm,user-code,fields"),
 ("Absurd","The JVM stores all value objects of one class in one memory location.","valhalla-jvm,user-code,array-api"),
 ("Absurd","The Clojure reader reads defvaluetype as defrecord.","clj-compiler,core-macro"),
 ("Absurd","All class names become 1 MB long.","loader,cap-probe,clj-compiler,value-transform"),
 ("Absurd","Each JVM start uses a random class-file major version.","valhalla-jvm,cap-probe,aot-output"),
 ("Absurd","The JVM refuses to load each class whose name contains 'Probe'.","cap-probe,capability-report"),
 ("Absurd","java.util.UUID/randomUUID returns the same value on every call.","cap-probe,loader"),
 ("Absurd","All arrays have length 0.","array-api,array-adapter"),
 ("Absurd","Every user believes that identity fallback classes are value classes.","user-code,docs"),
 ("Absurd","Constructors run after the methods of the object.","valhalla-jvm,value-transform,identity-backend,fields"),
 ("Absurd","GitHub deletes every repository with 'value' in its name.","release,source-jar,quality-ci,docs"),
 ("Absurd","The maintainer becomes 1000 people at the same time.","maintainer,release,ai-agents"),
 ("Absurd","System/getProperty returns a different value each time it is read.","runtime-policy,jvm-flags"),
 ("Absurd","All Clojure symbols become case-insensitive.","clj-compiler,fields,core-macro"),
]

# Step 6: stressors added for coverage gaps (before the split).
S_COVERAGE = [
 ("Technology","java.lang.classfile moves to a separate module that the JVM does not resolve by default.","classfile-api,value-transform,cap-probe,jvm-flags"),
 ("Suppliers and partners","Clojure updates its bundled clojure.asm and removes the ClassWriter constructor that value-type uses.","clojure-asm,identity-backend,cap-probe,clj-compiler"),
 ("Security","A CVE in java.lang.classfile makes operators disable it with a JVM flag.","classfile-api,value-transform,jvm-flags,app-author"),
 ("Data","A build tool caches macroexpanded value definitions and evaluates them on a different JDK.","expansion-transfer,loader,core-macro,aot-output"),
 ("Technology","An nREPL middleware sends macroexpanded forms from the editor to a remote JVM.","expansion-transfer,tooling,loader"),
 ("Technology","A new EA build removes the NullRestricted annotation. Native non-nil fields are not possible.","field-cap-probe,jdk-internal-value,fields,value-transform"),
 ("Physical world","A fire destroys the build machine during a release. It had the only copy of the benchmark results.","benchmarks,release,maintainer"),
 ("Society and politics","A popular blogger publishes benchmarks that show value-type slower than defrecord.","benchmarks,docs,lib-author"),
 ("Customers and users","Monitoring calls value-type.capability/report on each request and alerts on each change.","capability-report,cap-probe,field-cap-probe,array-adapter,app-author"),
 ("Absurd","clojure.asm and java.lang.classfile write the same bytes for every class.","clojure-asm,classfile-api,value-transform,identity-backend"),
 ("Society and politics","A licence dispute removes clojure.asm from Clojure distributions in one country.","clojure-asm,clj-compiler,identity-backend,app-author"),
 ("Physical world","A cosmic ray changes one byte of the field-capability probe class in memory.","field-cap-probe,capability-report,fields"),
]

S = S_INITIAL + S_COVERAGE
eids = [e[0] for e in ELEMENTS]
for c, _, a in S:
    for e in a.split(','):
        assert e in eids, e

def coverage():
    cats = collections.Counter(c for c, _, _ in S)
    els = collections.Counter(e for _, _, a in S for e in a.split(','))
    print(len(S), "stressors;", len(cats), "categories;", f"absurd {cats['Absurd']/len(S):.0%}")
    for c, n in sorted(cats.items(), key=lambda x: x[1]): print(f"  {n:3d} {c}")
    print("elements (ascending):")
    for e in sorted(eids, key=lambda e: els[e]): print(f"  {els[e]:3d} {e}")

if '--coverage' in sys.argv:
    coverage(); sys.exit(0)

# Step 7: split after coverage.
SEED = 202611062
ids = [f"S{i:03d}" for i in range(1, len(S) + 1)]
n_test = round(len(S) * 0.25)
test = set(random.Random(SEED).sample(ids, n_test))
with open('elements.tsv', 'w') as f:
    f.write(H('generate-stressors'))
    f.write("id\tname\tkind\tdescription\n")
    for e in ELEMENTS: f.write("\t".join(e) + "\n")
with open('stressors.tsv', 'w') as f:
    f.write(H('generate-stressors'))
    f.write(f"# split: random.Random({SEED}).sample, {n_test}/{len(S)} test (25%), date {DATE}, after coverage, before adaptation\n")
    f.write("id\tcategory\tstressor\taffects\tset\n")
    for sid, (c, s, a) in zip(ids, S):
        f.write(f"{sid}\t{c}\t{s}\t{a}\t{'test' if sid in test else 'training'}\n")
with open('connections.tsv', 'w') as f:
    f.write(H('find-hidden-coupling'))
    f.write("from\tto\n")
    for a, b in CONN: f.write(f"{a}\t{b}\n")
print(len(S), "stressors;", n_test, "test:", sorted(test))
