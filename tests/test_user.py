from __future__ import absolute_import
import unittest
from jarpis.user import *


class UserTest(unittest.TestCase):

    def setUp(self):
        User.createUserTable()

    def test_insert_user(self):
        user = User(None, "Hugo", 1)
        user.insertUser()
        self.assertEqual(user._name, "Hugo")

    def test_get_User_By_ID(self):
        user = User(1, "Hugo", 1)
        user.insertUser()
        result_user = User.getUserByID(1)
        self.assertIsNotNone(result_user)

    def test_not_get_User_By_ID(self):
        user = User(1, "Hugo", 1)
        user.insertUser()
        with self.assertRaises(UserNotFoundException):
            user.getUserByID(4)

    def test_delete_user(self):
        user = User(None, "Hugo", 1)
        user.insertUser()
        result_user = user.deleteUser()
        self.assertTrue(result_user)

    def test_delete_user1(self):
        user1 = User(1, "Hugo", 1)
        user1.insertUser()
        self.assertIsNotNone(User.getUserByID(1))
        user1.deleteUser()
        with self.assertRaises(UserNotFoundException):
            User.getUserByID(1)

    def test_get_User_from_Speaker(self):
        user = User(1, "Lausen", 1)
        user.insertUser()
        speaker = ("Lausen", 1)

        result = User.getUserFromSpeaker(speaker)
        self.assertEqual(result.id, 1)
        self.assertEqual(result.name, "Lausen")
        self.assertEqual(result.speakerID, 1)

    def test_speaker_has_no_user(self):
        user = User(1, "Lausen", 1)
        user.insertUser()
        speaker = ("Sperber", 0)

        with self.assertRaises(UserNotFoundException):
            User.getUserFromSpeaker(speaker)

    def tearDown(self):
        User.dropUserTable()
