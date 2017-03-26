from __future__ import absolute_import

import unittest
import jarpis.dialogs
from jarpis.user import User
from jarpis.dialogs.semantics import SemanticFrame, Slot
from jarpis.dialogs.discourse import DiscourseAnalysis
from mock import Mock, patch


class A_semantic_object_can_be_bound_to_a_user_entity(unittest.TestCase):

    def setUp(self):
        self._communication = jarpis.dialogs.communication

    def tearDown(self):
        del self._communication

    @patch("jarpis.user.User.getUserFromSpeaker")
    @patch("jarpis.recognition.speakerRecognition.get_current_speaker")
    def test_if_the_current_speaker_exists_as_user(self, mock_get_current_speaker, mock_getUserFromSpeaker):
        # arrange
        speaker = ("Dodo", 1)
        user = User(1, "Dodo", 1)
        mock_get_current_speaker.return_value = speaker
        mock_getUserFromSpeaker.return_value = user

        def handler(semantic_object):
            # assert
            self.assertEqual(semantic_object.semantic_class, "User")
            self.assertEqual(semantic_object.slots["name"].value, "Dodo")
            self.assertEqual(semantic_object.slots["name"].utterance, "me")

        handlerMock = Mock(wraps=handler)

        self._communication.register(
            "evaluationSuccessful", handlerMock)

        slots = {
            "name": Slot("Username", "name")
        }
        slots["name"].utterance = "me"
        semantic_object = SemanticFrame(None, "User", "UserByReference", slots)
        da = DiscourseAnalysis()

        # act
        da._bind_user(semantic_object)
