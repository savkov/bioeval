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

from utils import df2chunkset

__author__ = 'Aleksandar Savkov'

# ###### THE MATH ######
# precision = |correct chunks| / |guessed chunks|
# recall    = |correct chunks| / |gold chunks|
# f1 score  = 100 * 2 * precision * recall / (precision + recall)


def get_ncor(gold_chunks, guess_chunks):
    """Calculate the number of correctly overlapping chunks in the two sets.

    :param gold_chunks:
    :param guess_chunks:
    :return:
    """
    return set(x for x in list(set(gold_chunks) & set(guess_chunks)))


def evaluate(gold_sequence, guess_sequence, chunk_col=3, do_round=True):
    """Evaluate the f-score of the guess tagset based on a gold chunkset and a
    guess chunkset data structures.

    The assumption is simple. By transforming the list of tokens in a list of
    chunks (where only annotated chunks are not singletons), calculating the
    number of mismatches is as simple as a union of sets operation.

    Example data structure:

    example = {
        ((1, 'Gold', 'N', 'B-NP'),),
        ((2, 'is', 'V', 'B-MV'),),
        ((3, 'golden', 'J', 'B-AP'),),
        ((4, '.', '.', 'O'),),
        (
            (5, 'The', 'D', 'B-NP'),
            (6, 'red', 'J', 'I-NP'),
            (7, 'square', 'N', 'I-NP')
        ),
        ((8, 'is', 'V', 'B-MV'),),
        (
            (9, 'very', 'A', 'B-AP'),
            (10, 'large', 'J', 'I-AP')
        ),
        ((8, '.', '.', 'O'),)
    }

    :param gold_sequence: gold chunk sequence
    :type gold_sequence: set
    :param guess_sequence: guess chunk sequence
    :type guess_sequence: set
    :param chunk_col: gold column index
    :type chunk_col: int
    :param do_round: round the result to the second digit
    :type do_round: bool
    :return: f-score
    :rtype: float
    """

    gold_tags = [x for y in gold_sequence for x in y]
    guess_tags = [x for y in guess_sequence for x in y]

    assert len(gold_tags) == len(guess_tags), \
        'Non-matching number of tags %s!=%s.' % (len(gold_tags),
                                                 len(guess_tags))

    goch = [x for x in gold_sequence if x[0][chunk_col] != 'O']
    guch = [x for x in guess_sequence if x[0][chunk_col] != 'O']

    co = get_ncor(goch, guch)

    precision = len(co) / float(len(guch))
    recall = len(co) / float(len(goch))

    f1 = 2 * precision * recall / (precision + recall)

    if do_round:
        return round(100 * f1, 2), round(100 * precision, 2), \
               round(100 * recall, 2)
    else:
        return 100 * f1, 100 * precision, 100 * recall


def evaluate_df(df, chunkcol='chunktag', guesscol='guesstag', do_round=True):
    """Evaluates chunk annotation from a `pandas` `DataFrame`.

    :param df: dataframe
    :type df: pd.DataFrame
    :param chunkcol: the column name of the gold chunk tags
    :type chunkcol: str
    :param guesscol: the column name of the guess chunk tags
    :type guesscol: str
    :param do_round: round the results to second digit
    :type do_round: bool
    :return: f-score
    :rtype: float
    """

    go, ge = df2chunkset(df, chunkcol, guesscol)

    return evaluate(go, ge, 1, do_round)
