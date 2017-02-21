import unittest
from jarpis.event import *


class PrivacyTest(unittest.TestCase):

    def setUp(self):
        TestDBUtil.exec(Privacy.createPrivacyTable, [])
        TestDBUtil.exec()

    def testWhatEver(self):
        self.assertTrue(True)

    def tearDown(self):
        TestDBUtil.exec(Privacy.dropPrivacyTable,[])
