#!/usr/bin/env python3
"""Coupling counts for a stressor run record.

Usage: python3 coupling.py RUN_DIR [--min-similarity 0.5] [--min-shared 3] [--force]

Reads RUN_DIR/stressors.tsv (id, category, stressor, affects, set),
optional RUN_DIR/elements.tsv (id, ...) and RUN_DIR/connections.tsv (from, to).
Lines that start with '#' are skipped. Rows with set == 'test' are ignored.
Writes markdown to stdout. Exit 2 on invalid input, 3 on a failed mapping check
(unless --force).
"""
import argparse, csv, itertools, os, sys
from collections import defaultdict


def read_tsv(path):
    with open(path, newline='') as f:
        lines = [l for l in f if l.strip() and not l.startswith('#')]
    return list(csv.DictReader(lines, delimiter='\t'))


def load(run_dir):
    rows = read_tsv(os.path.join(run_dir, 'stressors.tsv'))
    epath = os.path.join(run_dir, 'elements.tsv')
    elements = [r['id'].strip() for r in read_tsv(epath)] if os.path.exists(epath) else None
    cpath = os.path.join(run_dir, 'connections.tsv')
    conns = [(r['from'].strip(), r['to'].strip()) for r in read_tsv(cpath)] if os.path.exists(cpath) else []
    return rows, elements, conns


def validate(rows, elements):
    errors, seen = [], set()
    for r in rows:
        sid = (r.get('id') or '').strip()
        if not sid:
            errors.append('a row has no id')
        elif sid in seen:
            errors.append(f'duplicate stressor id {sid}')
        seen.add(sid)
        if elements is not None:
            for e in split_affects(r):
                if e not in elements:
                    errors.append(f'{sid}: unknown element {e}')
    return errors


def split_affects(r):
    a = (r.get('affects') or '').strip()
    return [] if a in ('', 'none') else [e.strip() for e in a.split(',') if e.strip()]


def analyse(rows, conns, min_sim, min_shared):
    train = [r for r in rows if (r.get('set') or '').strip() != 'test']
    aff = {r['id'].strip(): set(split_affects(r)) for r in train}
    col = defaultdict(set)
    for s, es in aff.items():
        for e in es:
            col[e].add(s)
    elems = sorted(col)
    known = {frozenset(c) for c in conns}
    pairs, all_pairs = [], 0
    for a, b in itertools.combinations(elems, 2):
        all_pairs += 1
        sh, un = col[a] & col[b], col[a] | col[b]
        sim = len(sh) / len(un)
        if sim >= min_sim and len(sh) >= min_shared:
            pairs.append(dict(a=a, b=b, shared=sorted(sh), sim=sim,
                              known=frozenset((a, b)) in known))
    adj = defaultdict(set)
    for p in pairs:
        adj[p['a']].add(p['b']); adj[p['b']].add(p['a'])
    groups, seen = [], set()
    for e in sorted(adj):
        if e in seen:
            continue
        g, stack = set(), [e]
        while stack:
            x = stack.pop()
            if x not in g:
                g.add(x); stack.extend(adj[x] - g)
        seen |= g; groups.append(sorted(g))
    cset = set(conns)
    two_way = sorted({tuple(sorted(c)) for c in cset if (c[1], c[0]) in cset and c[0] != c[1]})
    return dict(aff=aff, col=col, elems=elems, pairs=pairs, all_pairs=all_pairs,
                groups=groups, two_way=two_way)


def mapping_check(res):
    """Return reasons why the mapping is too coarse or too fine. Empty list = pass."""
    n = len(res['aff'])
    reasons = []
    if n == 0:
        return ['no training stressors']
    for e in res['elems']:
        if len(res['col'][e]) > 0.8 * n:
            reasons.append(f'too coarse: {e} is affected by more than 80% of stressors')
    if res['all_pairs'] and len(res['pairs']) > 0.5 * res['all_pairs']:
        reasons.append('too coarse: more than 50% of element pairs are coupled')
    if not res['pairs']:
        reasons.append('too fine: no element pairs are coupled')
    single = sum(1 for es in res['aff'].values() if len(es) <= 1)
    if single > 0.8 * n:
        reasons.append('too fine: more than 80% of stressors affect one element or none')
    return reasons


def report(res, reasons, args, force):
    out = []
    col, aff = res['col'], res['aff']
    out.append(f"Training stressors: {len(aff)}. Elements: {len(res['elems'])}. "
               f"Limits: similarity >= {args.min_similarity}, shared >= {args.min_shared}.\n")
    out.append('## Mapping check\n')
    out.append('pass\n' if not reasons else 'FAIL\n\n' + '\n'.join(f'- {r}' for r in reasons) + '\n')
    out.append('## Vulnerable elements\n\n| Element | Count | Stressors |\n|---|---|---|')
    for e in sorted(res['elems'], key=lambda e: (-len(col[e]), e)):
        out.append(f"| {e} | {len(col[e])} | {', '.join(sorted(col[e]))} |")
    out.append('\n## Dangerous stressors (top 10 and ties)\n\n| ID | Elements |\n|---|---|')
    ranked = sorted(aff, key=lambda s: (-len(aff[s]), s))
    cut = len(aff[ranked[min(9, len(ranked) - 1)]]) if ranked else 0
    for s in ranked:
        if len(aff[s]) >= max(cut, 2):
            out.append(f'| {s} | {len(aff[s])} |')
    if reasons and not force:
        out.append('\nGroups not reported. Fix the mapping, then run again.')
        return '\n'.join(out)
    out.append('\n## Coupled pairs\n\n| A | B | Shared | Similarity | In design | Stressors |\n|---|---|---|---|---|---|')
    for p in sorted(res['pairs'], key=lambda p: (-p['sim'], -len(p['shared']), p['a'], p['b'])):
        k = 'yes' if p['known'] else 'no (hidden)'
        out.append(f"| {p['a']} | {p['b']} | {len(p['shared'])} | {p['sim']:.2f} | {k} | {', '.join(p['shared'])} |")
    out.append('\n## Groups\n')
    for g in res['groups']:
        shared = set.intersection(*(col[e] for e in g))
        out.append(f"- {', '.join(g)}: shared by all: {', '.join(sorted(shared)) or 'none'}")
    out.append('\n## Two-way dependencies\n')
    out.append('\n'.join(f'- {a} <-> {b}' for a, b in res['two_way']) or 'none')
    return '\n'.join(out)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('run_dir')
    ap.add_argument('--min-similarity', type=float, default=0.5)
    ap.add_argument('--min-shared', type=int, default=3)
    ap.add_argument('--force', action='store_true')
    args = ap.parse_args(argv)
    rows, elements, conns = load(args.run_dir)
    errors = validate(rows, elements)
    if errors:
        print('## Invalid input\n\n' + '\n'.join(f'- {e}' for e in errors))
        return 2
    res = analyse(rows, conns, args.min_similarity, args.min_shared)
    reasons = mapping_check(res)
    print(report(res, reasons, args, args.force))
    return 3 if reasons and not args.force else 0


if __name__ == '__main__':
    sys.exit(main())
