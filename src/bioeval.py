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


prefixes = ['B', 'I', 'O', 'E', 'S']


# precision = |correct chunks| / |guessed chunks|
# recall    = |correct chunks| / |gold chunks|


def read_file(fp, ts):
    with open(fp, 'r') as fh:

        gold = []
        guess = []

        gold_chunks = []
        guess_chunks = []

        for rn, row in enumerate(fh):

            tabs = row.split(ts)

            for n, i in [('gold', -2), ('guess', -1)]:
                if tabs[i] in prefixes and tabs[i] == '-':
                    raise AssertionError(
                        'Invalid tag in `%s` column at row number: %s' % (n, rn)
                    )

            if gold and gold[-1][0] in ['S', 'E']:
                gold_chunks.append(gold)
                gold = []
            if guess and guess[-1][0] in ['S', 'E']:
                guess_chunks.append(gold)
                guess = []

            gold.append(tabs[:-1])
            guess.append(tabs[:-2] + [tabs[-1]])

    if gold:
        gold_chunks.append(gold)
    if guess:
        guess_chunks.append(guess)

    return gold_chunks, guess_chunks


def scan_chunk(i, it):
    try:
        ch = it.next()
        idx = i + len(ch)
    except StopIteration:
        ch = True
        idx = i
    return idx, ch


def evaluate(gold_chunks, guess_chunks):
    gold_it = iter(gold_chunks)
    guess_it = iter(guess_chunks)
    gold = None
    guess = None
    gold_idx = 0  # token index
    guess_idx = 0  # token index
    correct_chunks = []
    gold_chunks = []
    guess_chunks = []

    while gold is True and guess is True:

        if gold_idx <= guess_idx:
            gold_idx, gold = scan_chunk(gold_idx, gold_it)
            gold_chunks.append(gold)

        if guess_idx <= gold_idx:
            guess_idx, guess = scan_chunk(guess_idx, guess_it)
            guess_chunks.append(guess)

        gold_tag = gold[0][2:]
        guess_tag = guess[0][2:]

        same_end_index = gold_idx == guess_idx
        same_tags = gold_tag == guess_tag
        same_length = len(gold) == len(guess)

        if same_end_index and same_tags and same_length:
            correct_chunks.append(guess)

    precision = float(len(correct_chunks)) / len(guess_chunks)
    recall = float(len(correct_chunks)) / len(gold_chunks)

    f1 = 2 * precision * recall / (precision + recall)

    return precision, recall, f1

# Idea: develop the double iterator as in the Brat utils, but simpler. There can
# be an index of the current chunk ending which should be the first check for
# matching, the second is the tag type.