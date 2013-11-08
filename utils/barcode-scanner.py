#!/usr/bin/env python

from codecs import open
import simplejson as json
import os.path
import uuid

from lxml import etree
from amazonproduct.api import API
from amazonproduct import errors

_here = os.path.dirname(os.path.abspath(__file__))
XSLT = os.path.join(_here, 'xml2json.xslt')


def jsonify(node):
    xslt_root = etree.parse(XSLT)
    transform = etree.XSLT(xslt_root)
    result = transform(node)
    return unicode(result)

if __name__ == '__main__':
    
    api = API(locale='de')
    collection = []
    while True:
        try:
            ean = raw_input('EAN? ')
            resp = api.item_lookup(ean, SearchIndex='All', IdType='EAN', ResponseGroup='Large')
            items = resp.Items.Item
            for item in items:
                attrs = item.ItemAttributes

                director = None
                if hasattr(attrs, 'Director'):
                    if len(attrs.Director) > 1:
                        director = [p.text for p in attrs.Director] 
                    else:
                        director = attrs.Director.text

                collection += [{
                    'id': str(uuid.uuid4()),
                    'ean': attrs.EAN.text,
                    'title': attrs.Title.text,
                    'type': attrs.Binding.text,
                    'meta': {
                        'asin': item.ASIN.text,
                        'director': director,
                        'actors': [p.text for p in attrs.Actor],
                        #'release date': attrs.ReleaseDate.text,
                    }
                }]
            print attrs.Title.text

            with open('collection.json', 'w', encoding='utf-8') as fp:
                json.dump(collection, fp)
        except errors.InvalidParameterValue:
            print 'ERROR'
        except EOFError:
            break
        except Exception, e:
            print e
            import pdb; pdb.set_trace()
            #pass