import re
from git import Repo
import sys

repo = Repo('.')

with open('setup.py') as fh:
    setup = fh.read()

repl = re.sub(r'(version\s*=\s*[\'"]\d+\.\d+\.\d+)\.dev0',
              r'version=\g<1>', setup)
m = re.search(r'version\s*=\s*[\'"](?P<v>\d+\.\d+\.\d+)', repl)
version = m.groupdict()['v']

if sys.argv[1] == 'prepare':
    with open('setup.py', 'w', encoding='utf-8') as fh:
        fh.write(repl)
    repo.index.add('setup.py')
    repo.commit(f'Released {version}')
    print('Ready to release!')

elif sys.argv[1] == 'initiate':
    major, middle, minor = version.split('.')
    version = f'{major}.{middle}.{int(minor) + 1}'
    new_setup = re.sub(f'{version}', f'{version}.dev0', repl)
    with open('setup.py', 'w') as fh:
        fh.write(new_setup)
    repo.index.add('setup.py')
    repo.index.commit(f'Starting development of {version}')
    print('Ready to push!')
