# -*- coding: utf-8 -*-

import unittest
import locator


class TestLocator(unittest.TestCase):

    def setUp(self):
        self.loc = locator.Locator(db='test_loc')
        self.loc.drop_database()

    def tearDown(self):
        self.loc.drop_database()

    def test_latest_position(self):
        self.loc.add_location('abc', 0, 0)
        lastest_id = self.loc.add_location('abc', 1, 1)
        ret = self.loc.get_lastest_location('abc')
        self.assertEqual(lastest_id, ret.id)
