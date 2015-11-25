"""
Unit tests for Driv
"""

# pylint: disable=protected-access,

import unittest
import sys
from src.config import LOGIN, LOGOUT, INVALID, CLEAR_CACHE, SET_CACHE, OPTIONS
import os
from src.drive import main
from src.drive_api import wf

class TestDrive(unittest.TestCase):
    """Unit tests of Drive"""


    def test_options(self):
        """Test if settings are displayed properly"""

        wf._items = []

        sys.argv = ['drive.py', '']
        main(None)
        self.assertEqual(len(wf._items), 2)
        self.assertEqual(wf._items[0].title, OPTIONS[0]['title'])
        self.assertEqual(wf._items[1].title, OPTIONS[1]['title'])
        wf._items = []


    def test_settings(self):
        """Test if settings are displayed properly"""

        wf._items = []

        sys.argv = ['drive.py', '>']
        main(None)
        self.assertEqual(len(wf._items), 4)
        self.assertEqual(wf._items[0].title, LOGIN['title'])
        self.assertEqual(wf._items[1].title, LOGOUT['title'])
        self.assertEqual(wf._items[2].title, CLEAR_CACHE['title'])
        self.assertEqual(wf._items[3].title, SET_CACHE['title'] % '[seconds]')
        wf._items = []

    def test_invalid_options(self):
        """Test if invalid option items is displayed"""

        wf._items = []

        sys.argv = ['drive.py', '> not here']
        main(None)
        self.assertEqual(len(wf._items), 1)
        self.assertEqual(wf._items[0].title, INVALID['title'])
        self.assertFalse(wf._items[0].valid)
        self.assertFalse(wf._items[0].arg)
        wf._items = []

    def test_login(self):
        """Test if login item is displayed"""

        sys.argv = ['drive.py', '> login']
        main(None)
        self.assertEqual(len(wf._items), 1)
        self.assertEqual(wf._items[0].title, LOGIN['title'])
        self.assertEqual(wf._items[0].arg, LOGIN['arg'])
        self.assertTrue(wf._items[0].valid)
        wf._items = []

        sys.argv = ['drive.py', '>login']
        main(None)
        self.assertEqual(len(wf._items), 1)
        self.assertEqual(wf._items[0].title, LOGIN['title'])
        self.assertEqual(wf._items[0].arg, LOGIN['arg'])
        self.assertTrue(wf._items[0].valid)
        wf._items = []

        sys.argv = ['drive.py', '>  login']
        main(None)
        self.assertEqual(len(wf._items), 1)
        self.assertEqual(wf._items[0].title, LOGIN['title'])
        self.assertEqual(wf._items[0].arg, LOGIN['arg'])
        self.assertTrue(wf._items[0].valid)
        wf._items = []

        sys.argv = ['drive.py', '>  Login']
        main(None)
        self.assertEqual(len(wf._items), 1)
        self.assertEqual(wf._items[0].title, LOGIN['title'])
        self.assertEqual(wf._items[0].arg, LOGIN['arg'])
        self.assertTrue(wf._items[0].valid)
        wf._items = []

        sys.argv = ['drive.py', '>  LOGIN']
        main(None)
        self.assertEqual(len(wf._items), 1)
        self.assertEqual(wf._items[0].title, LOGIN['title'])
        self.assertEqual(wf._items[0].arg, LOGIN['arg'])
        self.assertTrue(wf._items[0].valid)
        wf._items = []

    def test_logout(self):
        """Test if logout item is displayed properly"""

        wf._items = []

        sys.argv = ['drive.py', '> logout']
        main(None)
        self.assertEqual(len(wf._items), 1)
        self.assertEqual(wf._items[0].title, LOGOUT['title'])
        self.assertEqual(wf._items[0].arg, LOGOUT['arg'])
        self.assertTrue(wf._items[0].valid)
        wf._items = []

        sys.argv = ['drive.py', '>logout']
        main(None)
        self.assertEqual(len(wf._items), 1)
        self.assertEqual(wf._items[0].title, LOGOUT['title'])
        self.assertEqual(wf._items[0].arg, LOGOUT['arg'])
        self.assertTrue(wf._items[0].valid)
        wf._items = []

        sys.argv = ['drive.py', '>  logout']
        main(None)
        self.assertEqual(len(wf._items), 1)
        self.assertEqual(wf._items[0].title, LOGOUT['title'])
        self.assertEqual(wf._items[0].arg, LOGOUT['arg'])
        self.assertTrue(wf._items[0].valid)
        wf._items = []

        sys.argv = ['drive.py', '>  Logout']
        main(None)
        self.assertEqual(len(wf._items), 1)
        self.assertEqual(wf._items[0].title, LOGOUT['title'])
        self.assertEqual(wf._items[0].arg, LOGOUT['arg'])
        self.assertTrue(wf._items[0].valid)
        wf._items = []

        sys.argv = ['drive.py', '>  LOGOUT']
        main(None)
        self.assertEqual(len(wf._items), 1)
        self.assertEqual(wf._items[0].title, LOGOUT['title'])
        self.assertEqual(wf._items[0].arg, LOGOUT['arg'])
        self.assertTrue(wf._items[0].valid)
        wf._items = []

    def test_clear_cache(self):
        """Test if clear cache item is displayed properly"""

        wf._items = []

        sys.argv = ['drive.py', '> cl']
        main(None)
        self.assertEqual(len(wf._items), 1)
        self.assertEqual(wf._items[0].title, CLEAR_CACHE['title'])
        self.assertEqual(wf._items[0].arg, CLEAR_CACHE['arg'])
        self.assertTrue(wf._items[0].valid)
        wf._items = []

        sys.argv = ['drive.py', '> clear C']
        main(None)
        self.assertEqual(len(wf._items), 1)
        self.assertEqual(wf._items[0].title, CLEAR_CACHE['title'])
        self.assertEqual(wf._items[0].arg, CLEAR_CACHE['arg'])
        self.assertTrue(wf._items[0].valid)
        wf._items = []

        sys.argv = ['drive.py', '>cl']
        main(None)
        self.assertEqual(len(wf._items), 1)
        self.assertEqual(wf._items[0].title, CLEAR_CACHE['title'])
        self.assertEqual(wf._items[0].arg, CLEAR_CACHE['arg'])
        self.assertTrue(wf._items[0].valid)
        wf._items = []

        sys.argv = ['drive.py', '> clear cache']
        main(None)
        self.assertEqual(len(wf._items), 1)
        self.assertEqual(wf._items[0].title, CLEAR_CACHE['title'])
        self.assertEqual(wf._items[0].arg, CLEAR_CACHE['arg'])
        self.assertTrue(wf._items[0].valid)
        wf._items = []

    def test_set_cache(self):
        """Test if set cache item is displayed properly"""

        wf._items = []

        sys.argv = ['drive.py', '> set']
        main(None)
        self.assertEqual(len(wf._items), 1)
        self.assertEqual(wf._items[0].title, SET_CACHE['title'] % '[seconds]')
        self.assertFalse(wf._items[0].arg)
        self.assertFalse(wf._items[0].valid)
        wf._items = []

        sys.argv = ['drive.py', '> set C']
        main(None)
        self.assertEqual(len(wf._items), 1)
        self.assertEqual(wf._items[0].title, SET_CACHE['title'] % '[seconds]')
        self.assertFalse(wf._items[0].arg)
        self.assertFalse(wf._items[0].valid)
        wf._items = []

        sys.argv = ['drive.py', '>se']
        main(None)
        self.assertEqual(len(wf._items), 1)
        self.assertEqual(wf._items[0].title, SET_CACHE['title'] % '[seconds]')
        self.assertFalse(wf._items[0].arg)
        self.assertFalse(wf._items[0].valid)
        wf._items = []

        sys.argv = ['drive.py', '> set cache']
        main(None)
        self.assertEqual(len(wf._items), 1)
        self.assertEqual(wf._items[0].title, SET_CACHE['title'] % '[seconds]')
        self.assertFalse(wf._items[0].arg)
        self.assertFalse(wf._items[0].valid)
        wf._items = []

        sys.argv = ['drive.py', '> Set cache length 1']
        main(None)
        self.assertEqual(len(wf._items), 1)
        self.assertEqual(wf._items[0].title, SET_CACHE['title'] % '1 second')
        self.assertEqual(wf._items[0].arg, SET_CACHE['arg'] % str(1))
        self.assertTrue(wf._items[0].valid)
        wf._items = []

        sys.argv = ['drive.py', '> Set cache length 12']
        main(None)
        self.assertEqual(len(wf._items), 1)
        self.assertEqual(wf._items[0].title, SET_CACHE['title'] % '12 seconds')
        self.assertEqual(wf._items[0].arg, SET_CACHE['arg'] % str(12))
        self.assertTrue(wf._items[0].valid)
        wf._items = []

    def setUp(self):
        # supress stdout of feedback
        sys.stdout = open(os.devnull, 'w')

if __name__ == '__main__':
    unittest.main()
