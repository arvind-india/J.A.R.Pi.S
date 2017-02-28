from __future__ import absolute_import
import unittest
from jarpis.event import *


class PrivacyTest(unittest.TestCase):

    def setUp(self):
        TestDBUtil.execute(Privacy.createPrivacyTable, [])

    def test_get_state_id_by_name(self):
        self.assertEqual(TestDBUtil.execute(Privacy.getLevelsIdByName,["public"]),1)

    def test_get_state_name_by_id(self):
        self.assertEqual(TestDBUtil.execute(Privacy.getLevelsNameById,[1]), "public")

    def tearDown(self):
        TestDBUtil.execute(Privacy.dropPrivacyTable,[])
