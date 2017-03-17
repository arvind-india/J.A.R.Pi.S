from __future__ import absolute_import
import unittest
from jarpis.user import *


class UserTest(unittest.TestCase):

    def setUp(self):
        DBUtil.execute(User.createUserTable, [])

    def test_insert_user(self):
        user = User("Hugo")
        DBUtil.execute(user.insert, [])
        self.assertEqual(user._name, "Hugo")

    def tearDown(self):
        DBUtil.execute(User.dropUserTable, [])
