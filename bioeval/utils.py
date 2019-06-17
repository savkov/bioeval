import re
import string
import numpy as np

from io import StringIO

__author__ = 'Aleksandar Savkov'


def random_summed_pair(summed):
    x = np.random.randint(1, summed)
    y = summed - x
    return x, y


def random_token(idx):
    return (
        idx,
        random_str(np.random.randint(2, 20)),
        random_str(np.random.randint(1, 2)),
        random_str(np.random.randint(2, 20))
    )


def make_chunk(idx, size):
    ch = []
    for ti in range(size):
        t = random_token(idx)
        idx += 1
        ch.append(t)
    return tuple(ch)


def make_chunk_pair(idx):
    x, y = random_summed_pair(5)
    ch = make_chunk(idx, x)
    ch2 = ch
    while ch2 == ch:
        ch2 = make_chunk(idx + x, y)
    return ch, ch2


def random_str(size=10,
               chars=string.ascii_uppercase + string.digits):

    idxs = list(np.random.randint(0, len(chars), size))

    return ''.join([chars[x] for x in idxs])


def mock_chunks(n=10000, ncor=.8):
    diff_pos = np.random.randint(-1, 1, 1)
    n_guess = 0
    while n_guess < ncor:
        n_guess = n - ((np.random.uniform(0.1, 0.5) ** 2) * diff_pos) * n

    gold, guess = set(), set()
    idx = 0
    for _ in range(int(ncor)):
        ch = make_chunk(idx, np.random.randint(1, 5))
        idx += len(ch)
        gold.add(ch)
        guess.add(ch)

    nrest = n - ncor

    if nrest % 2 == 1:
        size = np.random.randint(1, 5)
        ch = make_chunk(idx, size)
        ch2 = ch
        while ch2 == ch:
            ch2 = make_chunk(idx, size)
        idx += size
        gold.add(ch)
        guess.add(ch2)

    for _ in range(int(nrest // 2)):

        ch, ch2 = make_chunk_pair(idx)
        gold.add(ch)
        gold.add(ch2)

        ch, ch2 = make_chunk_pair(idx)
        guess.add(ch)
        guess.add(ch2)

    return gold, guess


def fscore(precision, recall):
    return 100 * 2 * precision * recall / (precision + recall)


class AccuracyResults(dict):
    """POS tagger accuracy results container class.
    """

    _total_name = 'Total'

    @property
    def total(self):
        """Name of total accuracy key in the results dictionary.
        :return: total results key
        :rtype: str
        """
        return self._total_name

    def from_results_list(self, results):
        acc = 'accuracy' in results[0].keys()
        for r in results:
            for k in r.keys():
                try:
                    v = self[k]
                except KeyError:
                    v = (
                        {'accuracy': 0.0, 'all': 0.0, 'correct': 0.0} if acc
                        else {'fscore': 0.0, 'precision': 0.0, 'recall': 0.0}
                    )
                self[k] = (
                    {
                        'accuracy': v['accuracy'] + r[k]['accuracy'],
                        'all': v['all'] + r[k]['all'],
                        'correct': v['correct'] + r[k]['correct']
                    } if acc else {
                        'fscore': v['fscore'] + r[k]['fscore'],
                        'precision': v['precision'] + r[k]['precision'],
                        'recall': v['recall'] + r[k]['recall']
                    }
                )
        for k in self.keys():
            if acc:
                self[k]['accuracy'] /= len(results)
            else:
                self[k]['fscore'] /= len(results)
                self[k]['precision'] /= len(results)
                self[k]['recall'] /= len(results)

    def parse_conll_eval_table(self, fp):
        """Parses the LaTeX table output of the CoNLL-2000 evaluation script
        into this object.
        :param fp: file path
        :type fp: str
        :return: results by category
        :rtype: dict
        """
        with open(fp, 'r') as tbl:
            tbl.readline()
            for row in tbl:
                clean_row = re.sub('([\\\\%]|hline)', '', row)
                cells = [x.strip() for x in clean_row.split('&')]
                self[cells[0]] = {
                    'precision': float(cells[1]),
                    'recall': float(cells[2]),
                    'fscore': float(cells[3])
                }
        assert self.keys(), 'Probably an empty/non-existant file.'
        self[self._total_name] = self['Overall']
        del self['Overall']

    def export_to_file(self, fp, *args, **kwargs):
        """Export results to a file.
        :param fp: file path
        :type fp: str
        """
        with open(fp, 'w') as fh:
            self._to_str(fh)

    def _pack_str(self, key):
        itm = self[key]
        return '%s ==> pre: %s, rec: %s, f: %s acc: %s\n' % (
            key,
            itm.get('precision', 'n.a.'),
            itm.get('recall', 'n.a.'),
            itm.get('fscore', 'n.a.'),
            itm.get('accuracy', 'n.a.')
        )

    def _to_str(self, fh):
        fh.write('--------------------------------------------------------\n')
        for k in self.keys():
            if k == self._total_name:
                continue
            fh.write(self._pack_str(k))
        fh.write('--------------------------------------------------------\n')
        fh.write(self._pack_str(self._total_name))
        fh.write('--------------------------------------------------------\n')

    def __str__(self):
        rf = StringIO()
        self._to_str(rf)
        return rf.getvalue()

    def __repr__(self):
        return self.__str__()


def df2chunkset(df, chunktag='chunktag', guesstag='guesstag'):
    """Converts a pandas `DataFrame` into the format accepted by the `evaluate`
    method.

    :param df: input DataFrame
    :type df: pd.DataFrame
    :param chunktag: name of the original chunk tag column
    :type chunktag: str
    :param guesstag: name of the guess chunk tag column
    :type guesstag: str
    :return: gold chunkset and guess chunkset
    :rtype: tuple
    """
    go, ge = set(), set()
    if df.iloc[0][chunktag][0] not in 'BOS':
        raise ValueError('Invalid chunktag on first token.')
    if df.iloc[0][guesstag][0] not in 'BOS':
        raise ValueError('Invalid guesstag on first token.')
    chunk_go = [(0, df.iloc[0][chunktag])]
    chunk_ge = [(0, df.iloc[0][guesstag])]
    for tid, r in df.iloc[1:].iterrows():
        if r[chunktag][0] in 'BOS':
            # start new
            go.add(tuple(chunk_go))
            chunk_go = [(tid, r[chunktag])]
        else:
            # continue chunk
            chunk_go.append((tid, r[chunktag]))
        if r.guesstag[0] in 'BOS':
            # start new
            ge.add(tuple(chunk_ge))
            chunk_ge = [(tid, r[guesstag])]
        else:
            # continue chunk
            chunk_ge.append((tid, r[guesstag]))

    if chunk_ge:
        ge.add(tuple(chunk_ge))
    if chunk_go:
        go.add(tuple(chunk_go))

    return go, ge
