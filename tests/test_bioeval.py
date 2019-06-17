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

import os
import sys
import math
import warnings
import traceback
import pandas as pd

from unittest import TestCase
from bioeval import evaluate, evaluate_df, get_ncor
from bioeval.utils import *
from iterpipes3 import check_call, cmd

__author__ = 'Aleksandar Savkov'


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

        f1, pr, re = evaluate(gold, guess, do_round=False)

        self.assertAlmostEqual(f1, fscore(6.0/7, 6.0/6))

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
        f1_exact, _, _ = evaluate(gold, guess, do_round=False)

        self.assertEqual(f1, round(fscore(6.0/7, 6.0/7), 2))
        self.assertAlmostEqual(f1_exact, fscore(6.0/7, 6.0/7))

    def test_ncor(self):
        # change that to 1000+ if you want real testing
        rep = 10
        for i in range(rep):
            n = 10000
            ncor = math.floor(n * np.random.uniform(0.1, 1.0))
            gold, guess = mock_chunks(n=n, ncor=np.int(ncor))
            if len(gold) != len(guess):
                print(ncor, len(gold), len(guess))
                continue
            nc = len(get_ncor(gold, guess))
            self.assertAlmostEqual(nc, ncor, msg=(i,
                                                  len(gold),
                                                  len(guess),
                                                  nc,
                                                  ncor))

    def test_df(self):

        df = pd.DataFrame(
            [
                {'form': 'foo', 'pos': 'bar', 'chunktag': 'B-foo',
                 'guesstag': 'B-foo'},
                {'form': 'foo', 'pos': 'bar', 'chunktag': 'I-foo',
                 'guesstag': 'I-foo'},
                {'form': 'foo', 'pos': 'bar', 'chunktag': 'O', 'guesstag': 'O'},
                {'form': 'foo', 'pos': 'bar', 'chunktag': 'B-bar',
                 'guesstag': 'B-bar'},
                {'form': 'foo', 'pos': 'bar', 'chunktag': 'B-foo',
                 'guesstag': 'B-foo'},
                {'form': 'foo', 'pos': 'bar', 'chunktag': 'O', 'guesstag': 'O'},
                {'form': 'foo', 'pos': 'bar', 'chunktag': 'B-foo',
                 'guesstag': 'B-foo'},
                {'form': 'foo', 'pos': 'bar', 'chunktag': 'I-foo',
                 'guesstag': 'I-foo'},
                {'form': 'foo', 'pos': 'bar', 'chunktag': 'B-bar',
                 'guesstag': 'B-bar'},
                {'form': 'foo', 'pos': 'bar', 'chunktag': 'I-bar',
                 'guesstag': 'I-bar'},
                {'form': 'foo', 'pos': 'bar', 'chunktag': 'O', 'guesstag': 'O'},
                {'form': 'foo', 'pos': 'bar', 'chunktag': 'B-foo',
                 'guesstag': 'B-foo'},
                {'form': 'foo', 'pos': 'bar', 'chunktag': 'B-bar',
                 'guesstag': 'I-foo'},
                {'form': 'foo', 'pos': 'bar', 'chunktag': 'B-foo',
                 'guesstag': 'B-foo'},
                {'form': 'foo', 'pos': 'bar', 'chunktag': 'I-foo',
                 'guesstag': 'B-foo'}
            ]
        )

        f1, pr, re = evaluate_df(df, do_round=True)
        real_f1 = round(fscore(5/8, 5/8), 2)
        print(f1, real_f1)
        self.assertEqual(f1, real_f1)


class TestBIOEvalSpecial(TestCase):

    # make sure it runs from project root directory

    @staticmethod
    def _conll_eval(fp):
        """Evaluates a conll-style data file using the conll-2000 perl script.

        :param fp: file path
        :return: f1-score, precision, recall
        """

        cwd = '.'
        try:
            os.mkdir('tmp')
        except OSError:
            pass
        fpres = 'tmp/results.%s' % random_str()
        fh_out = open(fpres, 'w')

        if '\t' in open(fp, 'r').readline():
            warnings.warn('Wrong tab column separator. Use tabs (\\t).')

        try:
            check_call(cmd('perl prl/conll_eval.pl -l < {}', fp, cwd=cwd,
                           stdout=fh_out))
        except Exception:

            warnings.warn("Exception ocurred during Evaluation.")
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print("*** print_tb:")
            traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
            print("*** print_exception:")
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

    def test_against_conll2(self):

        fp = 'res/conll_sample.data'
        cols = ['form', 'pos', 'chunktag', 'guesstag']
        df = pd.read_csv(fp, sep=' ', names=cols)

        f1_conll, pre_conll, rec_conll = self._conll_eval(fp)

        f1, pre, rec = evaluate_df(df, do_round=True)

        self.assertEqual(f1, f1_conll)
        self.assertEqual(pre, pre_conll)
        self.assertEqual(rec, rec_conll)