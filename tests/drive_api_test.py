"""
Unit tests for Driv
"""

# pylint: disable=protected-access,

import unittest
import sys
from src.config import LOGIN, LOGOUT, INVALID, CLEAR_CACHE, SET_CACHE, FILES_URL, ERROR
from tests.sample_data import SAMPLE_ITEMS
import os
from src.drive_api import wf, Drive
import tests.httpretty as httpretty
import json
import src.requests as requests

CachedData = {}
Passwords = {}
StoredData = {}

class TestDrive(unittest.TestCase):
    """Unit tests of Drive"""

    def stest_get_links(self):
        """Test getting links for Google Drive API"""

        wf._items = []

        main(None)
        self.assertEqual(len(wf._items), 4)
        self.assertEqual(wf._items[0].title, LOGIN['title'])
        self.assertEqual(wf._items[1].title, LOGOUT['title'])
        self.assertEqual(wf._items[2].title, CLEAR_CACHE['title'])
        self.assertEqual(wf._items[3].title, SET_CACHE['title'] % '[seconds]')
        wf._items = []

    @httpretty.activate
    def dtesddt_show_items(self):
        httpretty.register_uri(httpretty.GET, FILES_URL, body=json.dumps({
            'items': SAMPLE_ITEMS
            }), content_type='application/json');

        Drive.show_items('c')
        self.assertEquals(len(wf._items), 21)
        wf._items = []

    @httpretty.activate
    def test_show_items_no_access_token(self):
        wf._items = []
        Drive.clear_cache()
        httpretty.register_uri(httpretty.GET, FILES_URL, body=exceptionCallback, content_type='text/html');
        self.assertEquals(len(wf._items), 0)
        Drive.show_items('c')
        self.assertEquals(len(wf._items), 1)
        self.assertEquals(wf._items[0].title, LOGIN['title'])

    @httpretty.activate
    def test_show_items_no_internet(self):
        wf.save_password('access_token', 'test')
        wf._items = []
        Drive.clear_cache()
        httpretty.register_uri(httpretty.GET, FILES_URL, body=exceptionCallback, content_type='text/html');
        self.assertEquals(len(wf._items), 0)
        Drive.show_items('c')
        self.assertEquals(len(wf._items), 1)
        self.assertEquals(wf._items[0].title, ERROR['ConnectionError']['title'])



    @httpretty.activate
    def stest_get_links(self):
        wf._items = []
        Drive.clear_cache()
        print 'wow'
        with self.assertRaises(Exception):
            Drive.get_links()


    def xtest_show_items_time(self):
        wf._items = []
        start_time = time.time() * 1000
        Drive.show_items('c')
        self.assertEquals(time.time() * 1000 - start_time, 0)

    def setUp(self):
        # sys.stdout = open(os.devnull, 'w')

        CachedData.clear()
        StoredData.clear()
        Passwords.clear()

        # replaces cache
        def cached_data(key, callback=None, max_age=None):
            """Save result of calling callback to cache"""
            if callback:
                CachedData[key] = callback()
            return CachedData.get(key)

        wf.cached_data = cached_data

        def store_data(key, value):
            """Save value in store"""
            StoredData[key] = value

        wf.store_data = store_data

        def stored_data(key):
            """Returns value from store"""
            try:
                return StoredData[key]
            except:
                return None

        wf.stored_data = stored_data

        def save_password(key, value):
            """Save value in password store"""
            Passwords[key] = value

        wf.save_password = save_password

        def get_password(key):
            """Returns value from password store"""
            return Passwords.get(key)

        wf.get_password = get_password

        def delete_password(key):
            """Delete password from password store"""
            if key in Passwords:
                del Passwords[key]

        wf.delete_password = delete_password

        # wf.save_password('venmo_access_token', SAMPLE_ACCESS_TOKEN)
        # wf.store_data('venmo_user', sample_user)


def exceptionCallback(request, uri, headers):
    raise requests.ConnectionError('Connection Error')

if __name__ == '__main__':
    unittest.main()
