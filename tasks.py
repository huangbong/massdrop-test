#!/usr/bin/env python3

import redis
import requests

def store_url_contents(id, url):
    """ Request and store the URL. """
    
    r = redis.Redis()
    resp = requests.get(url)
    result = resp.text
    r.set('rq:%s:result' % id, result)
    return resp.text