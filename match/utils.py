import re
non_an = re.compile(r'[^\w\s]')
collapse = re.compile(r'\s+')


def memoize(f):

    class memodict(dict):

        def __getitem__(self, *key):
            return dict.__getitem__(self, key)

        def __missing__(self, key):
            ret = self[key] = f(*key)
            return ret

    return memodict().__getitem__


"""
Text utils
"""

def clean_to_alphanum(s):
    if not s:
        return ''
    s = s.lower()
    s = non_an.sub('', s)
    s = collapse.sub(' ', s)
    return s.strip()
