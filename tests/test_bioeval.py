# This file is part of bioeval.
#
# bioeval is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# bioeval is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with bioeval.  If not, see <http://www.gnu.org/licenses/>.
__author__ = 'Aleksandar Savkov'

import os
import sys
import math
import string
import random
import warnings
import traceback
import numpy as np
from os.path import join
from unittest import TestCase
from bioeval import evaluate, _get_ncor
from iterpipes import check_call, cmd


class RandomData:

    @staticmethod
    def _random_summed_pair(sum):
        x = np.random.randint(1, sum)
        y = sum - x
        return x, y

    @staticmethod
    def _random_token(idx):
        return (
            idx,
            RandomData._random_str(np.random.randint(2, 20)),
            RandomData._random_str(np.random.randint(1, 2)),
            RandomData._random_str(np.random.randint(2, 20))
        )

    @staticmethod
    def _make_chunk(idx, size):
        ch = []
        for ti in range(size):
            t = RandomData._random_token(idx)
            idx += 1
            ch.append(t)
        return tuple(ch)

    @staticmethod
    def _make_chunk_pair(idx):
        x, y = RandomData._random_summed_pair(5)
        ch = RandomData._make_chunk(idx, x)
        ch2 = ch
        while ch2 == ch:
            ch2 = RandomData._make_chunk(idx + x, y)
        return ch, ch2

    @staticmethod
    def _random_str(size=10,
                    chars=string.ascii_uppercase + string.digits):
        return ''.join([chars[x]
                        for x
                        in np.random.randint(0, len(chars), size)])

    @staticmethod
    def fscore(precision, recall):
        return 100 * 2 * precision * recall / (precision + recall)

    @staticmethod
    def mock_chunks(n=10000, ncor=.8):
        diff_pos = np.random.randint(-1, 1, 1)
        n_guess = 0
        while n_guess < ncor:
            n_guess = n - ((np.random.uniform(0.1, 0.5) ** 2) * diff_pos) * n

        gold, guess = set(), set()
        idx = 0
        for _ in range(int(ncor)):
            ch = RandomData._make_chunk(idx, np.random.randint(1, 5))
            idx += len(ch)
            gold.add(ch)
            guess.add(ch)

        nrest = n - ncor

        if nrest % 2 == 1:
            size = np.random.randint(1, 5)
            ch = RandomData._make_chunk(idx, size)
            ch2 = ch
            while ch2 == ch:
                ch2 = RandomData._make_chunk(idx, size)
            idx += size
            gold.add(ch)
            guess.add(ch2)

        for _ in range(nrest/2):

            ch, ch2 = RandomData._make_chunk_pair(idx)
            gold.add(ch)
            gold.add(ch2)

            ch, ch2 = RandomData._make_chunk_pair(idx)
            guess.add(ch)
            guess.add(ch2)

        return gold, guess


class TestBIOEval(TestCase):

    def test_equality(self):
        gold = {
            ((1, 'Gold', 'N', 'B-NP'),),
            ((2, 'is', 'V', 'B-MV'),),
            ((3, 'green', 'J', 'B-AP'),),
            ((4, '.', '.', 'O'),),
            (
                (5, 'The', 'D', 'B-NP'),
                (6, 'red', 'J', 'I-NP'),
                (7, 'square', 'N', 'I-NP')
            ),
            ((8, 'is', 'V', 'B-MV'),),
            (
                (9, 'very', 'A', 'B-AP'),
                (10, 'boring', 'J', 'I-AP')
            ),
            ((8, '.', '.', 'O'),)
        }

        guess = {
            ((1, 'Gold', 'N', 'B-NP'),),
            ((2, 'is', 'V', 'B-MV'),),
            ((3, 'green', 'J', 'B-AP'),),
            ((4, '.', '.', 'O'),),
            (
                (5, 'The', 'D', 'B-NP'),
                (6, 'red', 'J', 'I-NP'),
                (7, 'square', 'N', 'I-NP')
            ),
            ((8, 'is', 'V', 'B-MV'),),
            (
                (9, 'very', 'A', 'B-AP'),
                (10, 'boring', 'J', 'I-AP')
            ),
            ((8, '.', '.', 'O'),)
        }

        f1, pr, re = evaluate(gold, guess)

        self.assertEqual(f1, 100)

    def test_one_diff(self):
        gold = {
            ((1, 'Gold', 'N', 'B-NP'),),
            ((2, 'is', 'V', 'B-MV'),),
            ((3, 'green', 'J', 'B-AP'),),
            ((4, '.', '.', 'O'),),
            (
                (5, 'The', 'D', 'B-NP'),
                (6, 'red', 'J', 'I-NP'),
                (7, 'square', 'N', 'I-NP')
            ),
            ((8, 'is', 'V', 'B-MV'),),
            (
                (9, 'very', 'A', 'B-AP'),
                (10, 'boring', 'J', 'I-AP')
            ),
            ((8, '.', '.', 'O'),)
        }

        guess = {
            ((1, 'Gold', 'N', 'B-NP'),),
            ((2, 'is', 'V', 'B-MV'),),
            ((3, 'green', 'J', 'B-AP'),),
            ((4, '.', '.', 'O'),),
            (
                (5, 'The', 'D', 'B-NP'),
                (6, 'red', 'J', 'I-NP'),
                (7, 'square', 'N', 'I-NP')
            ),
            ((8, 'is', 'V', 'B-MV'),),
            (
                (9, 'very', 'A', 'B-AP'),
                (10, 'boring', 'J', 'I-AP')
            ),
            ((8, '.', '.', '.'),)
        }

        f1, pr, re = evaluate(gold, guess)

        self.assertAlmostEqual(f1, RandomData.fscore(6.0/7, 6.0/6))

    def test_one_miss(self):
        gold = {
            ((1, 'Gold', 'N', 'B-NP'),),
            ((2, 'is', 'V', 'B-MV'),),
            ((3, 'green', 'J', 'B-AP'),),
            ((4, '.', '.', 'O'),),
            (
                (5, 'The', 'D', 'B-NP'),
                (6, 'red', 'J', 'I-NP'),
                (7, 'square', 'N', 'I-NP')
            ),
            ((8, 'is', 'V', 'B-MV'),),
            (
                (9, 'very', 'A', 'B-AP'),
                (10, 'boring', 'J', 'I-AP')
            ),
            ((8, '.', '.', 'O'),)
        }

        guess = {
            ((1, 'Gold', 'N', 'B-NP'),),
            ((2, 'is', 'V', 'B-MV'),),
            ((3, 'green', 'J', 'B-AP'),),
            ((4, '.', '.', 'O'),),
            (
                (5, 'The', 'D', 'B-NP'),
                (6, 'red', 'J', 'I-NP'),
                (7, 'square', 'N', 'I-NP')
            ),
            ((8, 'is', 'V', 'B-MV'),),
            (
                (9, 'very', 'A', 'B-AP'),
                (10, 'boring', 'J', 'I-AP')
            )
        }

        with self.assertRaises(AssertionError):
            evaluate(gold, guess)

    def test_one_diff_each(self):
        gold = {
            ((1, 'Gold', 'N', 'B-NP'),),
            ((2, 'is', 'V', 'B-MV'),),
            ((3, 'green', 'J', 'B-AP'),),
            ((4, '.', '.', 'B-NP'),),
            (
                (5, 'The', 'D', 'B-NP'),
                (6, 'red', 'J', 'I-NP'),
                (7, 'square', 'N', 'I-NP')
            ),
            ((8, 'is', 'V', 'B-MV'),),
            (
                (9, 'very', 'A', 'B-AP'),
                (10, 'boring', 'J', 'I-AP')
            ),
            ((8, '.', '.', 'O'),)
        }

        guess = {
            ((1, 'Gold', 'N', 'B-NP'),),
            ((2, 'is', 'V', 'B-MV'),),
            ((3, 'green', 'J', 'B-AP'),),
            ((4, '.', '.', 'O'),),
            (
                (5, 'The', 'D', 'B-NP'),
                (6, 'red', 'J', 'I-NP'),
                (7, 'square', 'N', 'I-NP')
            ),
            ((8, 'is', 'V', 'B-MV'),),
            (
                (9, 'very', 'A', 'B-AP'),
                (10, 'boring', 'J', 'I-AP')
            ),
            ((8, '.', '.', 'B-NP'),)
        }

        f1, pr, re = evaluate(gold, guess)

        self.assertEqual(f1, RandomData.fscore(6.0/7, 6.0/7))

    def test_ncor(self):
        # change that to 1000+ if you want real testing
        rep = 10
        for i in range(rep):
            n = 10000
            ncor = math.floor(n * np.random.uniform(0.1, 1.0))
            gold, guess = RandomData.mock_chunks(n=n, ncor=np.int(ncor))
            if len(gold) != len(guess):
                print ncor, len(gold), len(guess)
                continue
            nc = len(_get_ncor(gold, guess))
            self.assertAlmostEqual(nc, ncor, msg=(i,
                                                  len(gold),
                                                  len(guess),
                                                  nc,
                                                  ncor))

###############################################################################
# The following code block requires additional libraries to run. It is not
# essential for the testing process, although it is a good way to empirically
# confirm the tests with real-life redacted data.
###############################################################################


class TestBIOEvalSpecial(TestCase):

    # make sure it runs from project root directory

    @staticmethod
    def _conll_eval(fp):
        """Evaluates a conll-style data file using the conll-2000 perl script.

        :param fp: file path
        :return: f1-score, precision, recall
        """
        # library can be downloaded at https://github.com/savkov/ssvutils
        from ssvutils import AccuracyResults

        cwd = '.'
        fpres = 'tmp/results.%s' % RandomData._random_str()
        fh_out = open(fpres, 'w')

        if '\t' in open(fp, 'r').readline():
            warnings.warn('Wrong tab column separator. Use tabs (\\t).')

        try:
            check_call(cmd('perl prl/conll_eval.pl -l < {}', fp, cwd=cwd,
                           stdout=fh_out))
        except Exception:

            warnings.warn("Exception ocurred during Evaluation.")
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print "*** print_tb:"
            traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
            print "*** print_exception:"
            traceback.print_exception(exc_type, exc_value, exc_traceback,
                                      limit=2, file=sys.stdout)
        res = AccuracyResults()
        res.parse_conll_eval_table(fpres)
        os.remove(fpres)
        return res['Total']['fscore'], res['Total']['precision'], \
               res['Total']['recall']

    @staticmethod
    def _ssv2set(ssv):
        """Converts a SSVList with chunk tags and guess tags into two sets of
        chunk tuples -- gold and guess.

        :param ssv: data
        :return: :raise ValueError:
        """
        go, ge = set(), set()
        if ssv[0].chunktag[0] not in 'BOS':
            raise ValueError('Invalid chunktag on first token.')
        if ssv[0].guesstag[0] not in 'BOS':
            raise ValueError('Invalid guesstag on first token.')
        chunk_go = [(0, ssv[0].form, ssv[0].postag, ssv[0].chunktag)]
        chunk_ge = [(0, ssv[0].form, ssv[0].postag, ssv[0].guesstag)]
        for tid, r in enumerate(ssv[1:], start=1):
            if r.chunktag[0] in 'BOS':
                # start new
                go.add(tuple(chunk_go))
                chunk_go = [(tid, r.form, r.postag, r.chunktag)]
            else:
                # continue chunk
                chunk_go.append((tid, r.form, r.postag, r.chunktag))
            if r.guesstag[0] in 'BOS':
                # start new
                ge.add(tuple(chunk_ge))
                chunk_ge = [(tid, r.form, r.postag, r.guesstag)]
            else:
                # continue chunk
                chunk_ge.append((tid, r.form, r.postag, r.guesstag))

        if chunk_ge:
            ge.add(tuple(chunk_ge))
        if chunk_go:
            go.add(tuple(chunk_go))

        return go, ge

    def test_against_conll(self):
        """Tests empirically the performance of the this python implementation
        against the conll-2000 script.
        """
        # library can be downloaded at https://github.com/savkov/ssvutils
        from ssvutils import SSVList

        data = SSVList()
        data.parse_file('res/conll_sample.data', cols='chunkg', tab_sep=' ')

        # change that to 1000+ if you want real testing
        reps = 10

        results = []

        try:
            os.makedirs('tmp/')
        except OSError:
            pass

        n_seq = len(data.sequences)

        for size in list(np.random.randint(3, n_seq, reps)) + [n_seq]:

            fp = 'tmp/data.%s.data' % RandomData._random_str()
            b = SSVList([x for y in data.sequences[:size] for x in y])
            b.export_to_file(fp, cols='chunkg', tab_sep=' ')
            f1_conll, pr_conll, re_conll = self._conll_eval(fp)

            go, ge = self._ssv2set(b)
            for c in go:
                for t in c:
                    if len(t) < 4:
                        print c
            f1, pr, re = evaluate(go, ge)

            os.remove(fp)

            if not (f1_conll == round(f1, 2) and pr_conll == round(pr, 2) and
                            re_conll == round(re, 2)):
                print round(f1, 2), f1_conll, round(f1, 2) == f1_conll, \
                    round(pr, 2), pr_conll, pr_conll == round(pr, 2), \
                    round(re, 2), re_conll, re_conll == round(re, 2)

            results.append((round(f1, 2), f1_conll, round(f1, 2) == f1_conll,
                            round(pr, 2), pr_conll, pr_conll == round(pr, 2),
                            round(re, 2), re_conll, re_conll == round(re, 2)))

        wrong = len([x for x in results if not (x[2] and x[5] and x[8])])

        self.assertEqual(0, wrong, msg='%s wrong iterations out of %s' %
                                       (wrong, reps))