
"""
Collektr test server
====================

This is a stand-alone test server with a dummy data set to develop client
applications against.
"""

import json
import bottle
from . import filters, models

app = bottle.Bottle()
app.router.add_filter('uuid', filters.uuid_filter)
collection = models.Collection('collection.json')

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


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='localhost',
                        help='Hostname to use (default: %(default)s)')
    parser.add_argument('--port', type=int, default=8080,
                        help='Port to use (default: %(default)s)')
    parser.add_argument('--debug', action='store_true', default=False,
                        help='Turn bottle debugging on.')
    options = parser.parse_args()
    if options.debug:
        bottle.debug(True)
    app.run(host=options.host, port=options.port)
