# bioeval

[![CircleCI](https://circleci.com/gh/savkov/bioeval/tree/master.svg?style=svg&circle-token=a7c321334dce133af9fca534f186d8e5816ee1fc)](https://circleci.com/gh/savkov/bioeval/tree/master)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

CoNLL-2000 style evaluation of data using BIO and BEISO representation for 
mutli-token entities (i.e. chunks).

### Install

In the root folder execute:

`pip install bioeval`

### Change Log 

* [pypi release](https://pypi.org/project/bioeval/) and automated CI releases
* `bioeval` now supports pandas `DataFame` objects through `bioeval.evaluate_df`.

### Usage

The library supports two ways of evaluating span annotation. The first is the
native format way while the second uses a pandas DataFrame format.

#### Native input format

The native input format is a set of tuples, where each tuple signifies the 
group of tokens in a span. Tokens are also denoted by tuples that are supposed
to be unique. The user can achieve that uniqueness through adding a unique 
identifier to each token as in the example bellow.

```python
from bioeval import evaluate


# gold chunks
chunk = {
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
    ((11, '.', '.', 'O'),)
}

# candidate chunks
guess_chunk = {
    ((1, 'Gold', 'N', 'B-NP'),),
    ((2, 'is', 'V', 'I-NP'),),
    ((3, 'green', 'J', 'B-AP'),),
    ((4, '.', '.', 'B-NP'),),
    (
        (5, 'The', 'D', 'B-NP'),
        (6, 'red', 'J', 'I-NP')
    ),
    ((7, 'square', 'N', 'O'),),
    ((8, 'is', 'V', 'B-MV'),),
    (
        (9, 'very', 'A', 'B-AP'),
        (10, 'boring', 'J', 'I-AP')
    ),
    ((8, '.', '.', 'O'),)
}

# evaluation
f1, pr, re = evaluate(gold_sequence=chunk, guess_sequence=guess_chunk, chunk_col=3)
print(f1)
# 71.43
```

#### Dataframe format

The library supports dataframes input through the use of the `evaluate_df`
method, which needs the additional `chunkcol` and `guesscol` parameters to
specify the gold and candidate spans.

```python
import pandas as pd
from bioeval import evaluate_df

# input data as a JSON parsed to a DataFrame object
df = pd.DataFrame(
    [
        {'chunktag': 'B-foo','guesstag': 'B-foo'},
        {'chunktag': 'I-foo','guesstag': 'I-foo'},
        {'chunktag': 'O','guesstag': 'O'},
        {'chunktag': 'B-bar','guesstag': 'B-bar'},
        {'chunktag': 'B-foo','guesstag': 'B-foo'},
        {'chunktag': 'O','guesstag': 'O'},
        {'chunktag': 'B-foo','guesstag': 'B-foo'},
        {'chunktag': 'I-foo','guesstag': 'I-foo'},
        {'chunktag': 'B-bar','guesstag': 'B-bar'},
        {'chunktag': 'I-bar','guesstag': 'I-bar'},
        {'chunktag': 'O','guesstag': 'O'},
        {'chunktag': 'B-foo','guesstag': 'B-foo'},
        {'chunktag': 'B-bar','guesstag': 'I-foo'},
        {'chunktag': 'B-foo','guesstag': 'B-foo'},
        {'chunktag': 'I-foo','guesstag': 'B-foo'}
    ]
)

f1, pr, re = evaluate_df(df=df, chunkcol='chunktag', guesscol='guesstag')

print(f1)
>>> 62.5
```
