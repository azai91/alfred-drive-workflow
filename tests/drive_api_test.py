"""
Unit tests for Driv
"""

# pylint: disable=protected-access,

import unittest
import sys
from src.config import LOGIN, LOGOUT, INVALID, CLEAR_CACHE, SET_CACHE, FILES_URL, CONNECTION_ERROR
from tests.sample_data import SAMPLE_ITEMS
import os
from src.drive_api import wf, Drive
import tests.httpretty as httpretty
import json
import src.requests as requests
import time

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
    def test_show_items_error(self):
        wf._items = []
        Drive.clear_cache()
        httpretty.register_uri(httpretty.GET, FILES_URL, body=exceptionCallback, content_type='text/html');
        self.assertEquals(len(wf._items), 0)
        Drive.show_items('c')
        self.assertEquals(len(wf._items), 1)
        self.assertEquals(wf._items[0].title, CONNECTION_ERROR['title'])

    def test_show_items_time(self):
        wf._items = []
        start_time = time.time() * 1000
        Drive.show_items('c')
        self.assertEquals(time.time() * 1000 - start_time, 0)

    def setUp(self):
        sys.stdout = open(os.devnull, 'w')


def exceptionCallback(request, uri, headers):
    raise requests.ConnectionError('Connection Error')

if __name__ == '__main__':
    unittest.main()
