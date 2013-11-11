
"""
Collektr test server
====================

This is a stand-alone test server with a dummy data set to develop client
applications against.
"""

import json
import os
import re

import bottle

app = bottle.Bottle()

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

collection = Collection('collection.json')


def uuid_filter(config):
    """
    Matches a valid UUID.
    """
    regexp = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
    def to_python(match):
        return match
    def to_url(uri):
        return uri
    return regexp, to_python, to_url

app.router.add_filter('uuid', uuid_filter)


@app.hook('before_request')
def set_json_header():
    # Change header for all responses
    bottle.response.content_type = 'application/json; charset=utf-8'

@app.route('/')
def index():
    bottle.redirect('/collection/')

@app.get('/collection/')
def show_all_my_items():
    return json.dumps(collection.data)

@app.get('/collection/<item_id:uuid>/')
def show_singe_item(item_id):
    try:
        return json.dumps(collection[item_id])
    except KeyError:
        raise bottle.HTTPError(404)

@app.get('/collection/<item_id:uuid>/history/')
def show_item_history(item_id): pass

@app.post('/collection/')
@app.post('/collection/add/')
def add_new_item(): pass

@app.post('/collection/<item_id:uuid>/lend/')
def lend_item_to_user(item_id): pass

@app.post('/collection/<item_id:uuid>/borrow/')
def borrow_item_from_user(item_id): pass

@app.post('/collection/<item_id:uuid>/return/')
def return_item_to_owner(item_id): pass

@app.delete('/collection/<item_id:uuid>/')
def delete_item(item_id): pass

@app.route(r'/cover/<ean:re:\d{13}>')
def callback(ean):
    return bottle.static_file('%s.jpg' % ean, COVERS_DIR)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='localhost',
                        help='Hostname to use (default: %(default)s)')
    parser.add_argument('--port', type=int, default=8080,
                        help='Port to use (default: %(default)s)')
    parser.add_argument('--debug', action='store_true', default=False,
                        help='Turn bottle debugging on.')
    options = parser.parse_args()
    if options.debug: bottle.debug(True)
    app.run(host=options.host, port=options.port)
