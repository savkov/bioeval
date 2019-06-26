import re
from git import Repo

with open('setup.py') as fh:
    setup = fh.read()

repl = re.sub(r'(version\s*=\s*[\'"]\d+\.\d+\.\d+)\.dev0', 'version=\1', setup)
m = re.match(r'.*version\s*=\s*(?P<v>[\'"]\d+\.\d+\.\d+)\.dev0.*', setup)
version = m.groupdict()['v']

with open('setup.py', 'w', encoding='utf-8') as fh:
    fh.write(repl)

repo = Repo('.')

repo.index.add('setup.py')
repo.commit(f'Released {version}')

major, middle, minor = version.split('.')
version = f'{major}.{middle}.{int(minor) + 1}'
new_setup = re.sub(f'{version}', f'{version}.dev0', repl)

with open('setup.py', 'w') as fh:
    fh.write(new_setup)

repo.index.add('setup.py')
repo.index.commit(f'Starting development of {version}')

print('All done!')
