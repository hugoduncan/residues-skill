"""Split stressors and run the find-hidden-coupling counts. Deterministic (seed 42)."""
import csv, random, itertools, sys
from collections import defaultdict

rows = list(csv.DictReader(open('stressors.tsv'), delimiter='\t'))
ids = [r['id'] for r in rows]
test = set(random.Random(42).sample(ids, 15))

if sys.argv[1:] == ['split']:
    with open('split.tsv', 'w') as f:
        f.write('id\tset\n')
        for i in ids:
            f.write(f"{i}\t{'test' if i in test else 'training'}\n")
    print(f"training={len(ids)-len(test)} test={len(test)} (test IDs written to split.tsv)")
    sys.exit()

train = [r for r in rows if r['id'] not in test]
aff = {r['id']: set(r['affects'].split(',')) for r in train}
elems = sorted({e for s in aff.values() for e in s})
col = defaultdict(set)
for s, es in aff.items():
    for e in es:
        col[e].add(s)

known = set()
edges = """gs design-in gen-tables model context desc elements stressors affects test-mark
fhc stressors affects elements limits code-tool design-in groups gs
ad design-in stressors groups essentials test-mark survive model naive adapted decisions
adapted ad
ed naive adapted stressors test-mark essentials survive ri gs
harness desc repo model
user design-in essentials decisions
fhc model context
ad context
ed model context"""
for line in edges.splitlines():
    a, *bs = line.split()
    for b in bs:
        known.add(frozenset((a, b)))

print("## Vulnerable elements\n\n| Element | Count | Stressors |\n|---|---|---|")
for e in sorted(elems, key=lambda e: (-len(col[e]), e)):
    print(f"| {e} | {len(col[e])} | {', '.join(sorted(col[e]))} |")

print("\n## Dangerous stressors (≥ 5 elements)\n\n| ID | Elements | Stressor |\n|---|---|---|")
byid = {r['id']: r for r in train}
for s in sorted(aff, key=lambda s: (-len(aff[s]), s)):
    if len(aff[s]) >= 5:
        print(f"| {s} | {len(aff[s])} | {byid[s]['stressor']} |")

print("\n## Coupled pairs (similarity ≥ 0.5, shared ≥ 3)\n\n| A | B | Shared | Similarity | In design | Stressors |\n|---|---|---|---|---|---|")
pairs = []
for a, b in itertools.combinations(elems, 2):
    sh = col[a] & col[b]; un = col[a] | col[b]
    sim = len(sh) / len(un)
    if sim >= 0.5 and len(sh) >= 3:
        pairs.append((a, b, len(sh), sim, sh))
for a, b, n, sim, sh in sorted(pairs, key=lambda p: (-p[3], -p[2])):
    k = 'yes' if frozenset((a, b)) in known else 'no (hidden)'
    print(f"| {a} | {b} | {n} | {sim:.2f} | {k} | {', '.join(sorted(sh))} |")

print("\n## Near pairs (similarity ≥ 0.4, shared ≥ 3, below limit)\n\n| A | B | Shared | Similarity | In design |\n|---|---|---|---|---|")
for a, b in itertools.combinations(elems, 2):
    sh = col[a] & col[b]; un = col[a] | col[b]; sim = len(sh) / len(un)
    if 0.4 <= sim < 0.5 and len(sh) >= 3:
        k = 'yes' if frozenset((a, b)) in known else 'no (hidden)'
        print(f"| {a} | {b} | {len(sh)} | {sim:.2f} | {k} |")

# groups = connected components of coupled pairs
adj = defaultdict(set)
for a, b, *_ in pairs:
    adj[a].add(b); adj[b].add(a)
seen, groups = set(), []
for e in adj:
    if e in seen: continue
    stack, g = [e], set()
    while stack:
        x = stack.pop()
        if x in g: continue
        g.add(x); stack.extend(adj[x] - g)
    seen |= g; groups.append(sorted(g))
print("\n## Groups\n")
for g in groups:
    shared = set.intersection(*(col[e] for e in g))
    print(f"- {', '.join(g)} — stressors shared by all: {', '.join(sorted(shared)) or 'none'}")

print("\n## Elements with no training stressor\n")
allel = "user model harness context code-tool repo desc gs fhc ad ed gen-tables limits design-in elements stressors affects test-mark groups essentials survive naive adapted ri decisions".split()
print(', '.join(e for e in allel if e not in col) or 'none')
