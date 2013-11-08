
"""

"""

import json
import os.path

import bottle

app = bottle.Bottle()

_here = os.path.dirname(os.path.abspath(__file__))
FIXTURES_DIR = os.path.join(_here, 'fixtures')
COVERS_DIR = os.path.join(_here, 'covers')

collection = json.load(open(os.path.join(FIXTURES_DIR, 'collection.json')))

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

@app.route('/')
def index():
    return 'Hello!'

@app.get('/collection/')
def show_my_items():
    bottle.response.content_type = 'application/json; charset=utf-8'
    return json.dumps(collection)

@app.get('/collection/<item_id:uuid>/')
def show_item(item_id):
    bottle.response.content_type = 'application/json; charset=utf-8'
    return json.dumps(collection)

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

@app.route('/cover/<ean:re:\d{13}>')
def callback(ean):
    return bottle.static_file(os.path.join(COVERS_DIR, '%s.jpg' % ean))

if __name__ == '__main__':
    bottle.debug(True)
    app.run(host='localhost', port=8080)