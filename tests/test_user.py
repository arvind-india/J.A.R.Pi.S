from __future__ import absolute_import
import unittest
from jarpis.user import *


class UserTest(unittest.TestCase):

    def setUp(self):
        DBUtil.execute(User.createUserTable, [])

    def test_insert_user(self):
        user = User(None, "Hugo", 1)
        DBUtil.execute(user.insertUser, [])
        self.assertEqual(user._name, "Hugo")

    def test_get_User_By_ID(self):
        user = User(1, "Hugo", 1)
        DBUtil.execute(user.insertUser, [])
        result_user = DBUtil.execute(User.getUserByID, [1])
        self.assertIsNotNone(result_user)

    def test_not_get_User_By_ID(self):
        user = User(1, "Hugo", 1)
        DBUtil.execute(user.insertUser, [])
        with self.assertRaises(UserNotFoundException):
            DBUtil.execute(user.getUserByID, [4])

    def test_delete_user(self):
        user = User(None, "Hugo", 1)
        DBUtil.execute(user.insertUser, [])
        result_user = DBUtil.execute(user.deleteUser, [])
        self.assertTrue(result_user)

    def test_delete_user1(self):
        user1 = User(1, "Hugo", 1)
        DBUtil.execute(user1.insertUser, [])
        self.assertIsNotNone(DBUtil.execute(User.getUserByID, [1]))
        DBUtil.execute(user1.deleteUser, [])
        with self.assertRaises(UserNotFoundException):
            DBUtil.execute(User.getUserByID, [1])

    def tearDown(self):
        DBUtil.execute(User.dropUserTable, [])
