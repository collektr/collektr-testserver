
import json
import os
import re

_here = os.path.dirname(os.path.abspath(__file__))
FIXTURES_DIR = os.path.join(_here, 'fixtures')
COVERS_DIR = os.path.join(_here, 'covers')


class Collection(object):

    def __init__(self, fixtures=None):
        self._index = {}
        cover_reg = re.compile(r'^(\d{13})\.(jpe?g|gif|png)$', re.I)
        self.covers = {}
        for cover in os.listdir(COVERS_DIR):
            basename = os.path.basename(cover)
            m = cover_reg.match(basename)
            if m:
                self.covers[m.group(1)] = '/cover/%s' % m.group(1)
        if fixtures:
            path = os.path.join(FIXTURES_DIR, fixtures)
            self.data = json.load(open(path))
            for entry in self.data:
                self._index[entry['ean']] = entry
                self._index[entry['id']] = entry
                if entry['ean'] in self.covers:
                    entry['cover'] = self.covers[entry['ean']]

    def __getitem__(self, key):
        return self._index[key]
