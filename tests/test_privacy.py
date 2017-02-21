import unittest
from jarpis.event import *


class PrivacyTest(unittest.TestCase):

    def setUp(self):
        TestDBUtil.exec(Privacy.createPrivacyTable, [])

    def testGetStateIdByName(self):
        self.assertEqual(TestDBUtil.exec(Privacy.getTypeIdByName,["public"]),1)

    def testGetStateNameById(self):
        self.assertEqual(TestDBUtil.exec(Privacy.getTypeNameById,[1]), "public")

    def tearDown(self):
        TestDBUtil.exec(Privacy.dropPrivacyTable,[])
