# bioeval
CoNLL-2000 style evaluation of data using BIO and BEISO representation for 
mutli-token entities (i.e. chunks).

### Change Log 

* `bioeval` now supports pandas `DataFame` objects through `bioeval.evaluate_df`.

Example:

```python
import pandas as pd
from bioeval import evaluate_df

# form and POS tags are not necessary
df = pd.DataFrame(
    [
        {'form': 'foo', 'pos': 'bar', 'chunktag': 'B-foo','guesstag': 'B-foo'},
        {'form': 'foo', 'pos': 'bar', 'chunktag': 'I-foo','guesstag': 'I-foo'},
        {'form': 'foo', 'pos': 'bar', 'chunktag': 'O','guesstag': 'O'},
        {'form': 'foo', 'pos': 'bar', 'chunktag': 'B-bar','guesstag': 'B-bar'},
        {'form': 'foo', 'pos': 'bar', 'chunktag': 'B-foo','guesstag': 'B-foo'},
        {'form': 'foo', 'pos': 'bar', 'chunktag': 'O','guesstag': 'O'},
        {'form': 'foo', 'pos': 'bar', 'chunktag': 'B-foo','guesstag': 'B-foo'},
        {'form': 'foo', 'pos': 'bar', 'chunktag': 'I-foo','guesstag': 'I-foo'},
        {'form': 'foo', 'pos': 'bar', 'chunktag': 'B-bar','guesstag': 'B-bar'},
        {'form': 'foo', 'pos': 'bar', 'chunktag': 'I-bar','guesstag': 'I-bar'},
        {'form': 'foo', 'pos': 'bar', 'chunktag': 'O','guesstag': 'O'},
        {'form': 'foo', 'pos': 'bar', 'chunktag': 'B-foo','guesstag': 'B-foo'},
        {'form': 'foo', 'pos': 'bar', 'chunktag': 'B-bar','guesstag': 'I-foo'},
        {'form': 'foo', 'pos': 'bar', 'chunktag': 'B-foo','guesstag': 'B-foo'},
        {'form': 'foo', 'pos': 'bar', 'chunktag': 'I-foo','guesstag': 'B-foo'}
    ]
)

f1, pr, re = evaluate_df(df, 'chunktag', 'guesstag')

print(f1)
>>> 62.5
```

### Input format

```python
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
    ((8, '.', '.', 'O'),)
}
```


### Install

In the root folder execute:

`pip install -r requirements.txt .`

