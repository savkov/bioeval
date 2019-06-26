import re
from git import Repo
import sys

repo = Repo('.')

with open('setup.py') as fh:
    setup = fh.read()

if sys.argv[1] == 'prepare':
    repl = re.sub(r'(version\s*=\s*[\'"]\d+\.\d+\.\d+)\.dev0', r'\g<1>', setup)
    m = re.search(r'version\s*=\s*[\'"](?P<v>\d+\.\d+\.\d+)', repl)
    version = m.groupdict()['v']
    with open('setup.py', 'w', encoding='utf-8') as fh:
        fh.write(repl)
    repo.index.add(['setup.py'])
    repo.index.commit(f'Released {version}')
    print('Ready to release!')

elif sys.argv[1] == 'initiate':
    m = re.search(r'version\s*=\s*[\'"](?P<v>\d+\.\d+\.\d+)', setup)
    version = m.groupdict()['v']
    major, middle, minor = version.split('.')
    new_version = f'{major}.{middle}.{int(minor) + 1}'
    new_setup = re.sub(f'{version}', f'{new_version}.dev0', setup)
    with open('setup.py', 'w') as fh:
        fh.write(new_setup)
    repo.index.add(['setup.py'])
    repo.index.commit(f'Starting development of {new_version}')
    print('Ready to push!')
