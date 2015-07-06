# This file is part of BIOEval.
#
# BIOEval is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# BIOEval is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with BIOEval.  If not, see <http://www.gnu.org/licenses/>.
__author__ = 'Aleksandar Savkov'

# precision = |correct chunks| / |guessed chunks|
# recall    = |correct chunks| / |gold chunks|
# f1 score  = 100 * 2 * precision * recall / (precision + recall)


def _get_ncor(gold_chunks, guess_chunks):
    return set(x for x in list(set(gold_chunks) & set(guess_chunks)))


def evaluate(gold_chunks, guess_chunks, chunk_col=3, do_round=True):

    gold_tags = [x for y in gold_chunks for x in y]
    guess_tags = [x for y in guess_chunks for x in y]

    assert len(gold_tags) == len(guess_tags), \
        'Non-matching number of tags %s!=%s.' % (len(gold_tags),
                                                 len(guess_tags))

    goch = [x for x in gold_chunks if x[0][chunk_col] != 'O']
    guch = [x for x in guess_chunks if x[0][chunk_col] != 'O']

    co = _get_ncor(goch, guch)

    precision = len(co) / float(len(guch))
    recall = len(co) / float(len(goch))

    f1 = 2 * precision * recall / (precision + recall)

    if do_round:
        return round(100 * f1, 2), round(100 * precision, 2), \
               round(100 * recall, 2)
    else:
        return 100 * f1, 100 * precision, 100 * recall