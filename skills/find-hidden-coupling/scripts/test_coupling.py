"""Tests for coupling.py with known matrices. Run: python3 -m unittest test_coupling.py"""
import contextlib, io, os, sys, tempfile, unittest
sys.path.insert(0, os.path.dirname(__file__))
import coupling


def run_dir(stressors, elements=None, connections=None):
    d = tempfile.mkdtemp()
    with open(os.path.join(d, 'stressors.tsv'), 'w') as f:
        f.write('# run: t | date: 2026-11-06 | skill: test\n')
        f.write('id\tcategory\tstressor\taffects\tset\n')
        for sid, affects, s in stressors:
            f.write(f'{sid}\tc\tevent\t{affects}\t{s}\n')
    if elements is not None:
        with open(os.path.join(d, 'elements.tsv'), 'w') as f:
            f.write('id\tname\n' + ''.join(f'{e}\t{e}\n' for e in elements))
    if connections is not None:
        with open(os.path.join(d, 'connections.tsv'), 'w') as f:
            f.write('from\tto\n' + ''.join(f'{a}\t{b}\n' for a, b in connections))
    return d


def call(d, *args):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        code = coupling.main([d, *args])
    return code, buf.getvalue()


KNOWN = [
    ('S1', 'a,b', 'training'), ('S2', 'a,b', 'training'), ('S3', 'a,b,c', 'training'),
    ('S4', 'c,d', 'training'), ('S5', 'd,e', 'training'), ('S6', 'e,f', 'training'),
    ('S7', 'a,b,c,d,e,f', 'test'),
]


class CouplingTest(unittest.TestCase):
    def test_known_matrix(self):
        d = run_dir(KNOWN, elements='abcdef', connections=[('c', 'd'), ('d', 'c')])
        rows, el, conns = coupling.load(d)
        res = coupling.analyse(rows, conns, 0.5, 3)
        self.assertEqual([(p['a'], p['b'], p['shared'], p['known']) for p in res['pairs']],
                         [('a', 'b', ['S1', 'S2', 'S3'], False)])
        self.assertEqual(res['groups'], [['a', 'b']])
        self.assertEqual(res['two_way'], [('c', 'd')])
        self.assertNotIn('S7', res['aff'])  # test rows ignored

    def test_dangerous_top_ten_with_ties(self):
        rows = [(f'S{i:02}', 'a,b,c' if i < 12 else 'a,b', '') for i in range(20)]
        _, out = call(run_dir(rows), '--force')
        section = out.split('## Dangerous stressors')[1].split('##')[0]
        self.assertEqual(section.count('| S'), 12)

    def test_known_pair_marked(self):
        d = run_dir(KNOWN, connections=[('a', 'b')])
        _, out = call(d)
        self.assertIn('| a | b | 3 | 1.00 | yes |', out)

    def test_duplicate_id_and_unknown_element(self):
        d = run_dir([('S1', 'a', ''), ('S1', 'x', '')], elements='a')
        code, out = call(d)
        self.assertEqual(code, 2)
        self.assertIn('duplicate stressor id S1', out)
        self.assertIn('unknown element x', out)

    def test_too_coarse(self):
        d = run_dir([(f'S{i}', 'a,b,c', '') for i in range(5)])
        code, out = call(d)
        self.assertEqual(code, 3)
        self.assertIn('too coarse', out)
        self.assertIn('Groups not reported', out)

    def test_too_fine(self):
        d = run_dir([(f'S{i}', f'e{i}', '') for i in range(5)])
        code, out = call(d)
        self.assertEqual(code, 3)
        self.assertIn('too fine', out)

    def test_force_reports_groups(self):
        d = run_dir([(f'S{i}', 'a,b,c', '') for i in range(5)])
        code, out = call(d, '--force')
        self.assertEqual(code, 0)
        self.assertIn('## Groups', out)


if __name__ == '__main__':
    unittest.main()
