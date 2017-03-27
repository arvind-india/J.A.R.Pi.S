from __future__ import absolute_import

import unittest
from datetime import datetime, timedelta
from jarpis.user import User
from jarpis.dialogs.events import EventMediator
from jarpis.dialogs.semantics import SemanticFrame, Slot
from jarpis.dialogs.discourse import DiscourseAnalysis
from mock import Mock, patch


class A_semantic_object_can_be_bound_to_a_user_entity(unittest.TestCase):

    def setUp(self):
        self._communication = EventMediator()

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
            "reference": Slot("Reference", "reference", SemanticFrame(None, "Reference", "Reference"))
        }
        slots["reference"].semantic_frame.utterance = "me"
        semantic_object = SemanticFrame(None, "User", "UserByReference", slots)
        da = DiscourseAnalysis()

        # act
        da._bind_user(semantic_object)


class A_semantic_object_can_be_bound_to_a_date_entity(unittest.TestCase):

    def setUp(self):
        self._communication = EventMediator()

    def tearDown(self):
        del self._communication

    @patch("jarpis.calendar.Calendar.getDateByOffset")
    @patch("jarpis.calendar.Calendar.getCurrentDate")
    def test_if_the_date_is_referenced_as_today(self, mock_current_date, mock_offset_date):
        # arrange
        mock_current_date.return_value = datetime.today()
        zero_offset = timedelta(days=0)
        mock_offset_date.return_value = mock_current_date.return_value + zero_offset

        def handler(semantic_object):
            # assert
            self.assertEqual(semantic_object.semantic_class, "Date")
            self.assertEqual(semantic_object.slots[
                             "timestamp"].value, mock_offset_date.return_value.isoformat())
            self.assertEqual(semantic_object.slots[
                             "timestamp"].utterance, "today")

        handlerMock = Mock(wraps=handler)

        self._communication.register(
            "evaluationSuccessful", handlerMock)

        slots = {
            "reference": Slot("Reference", "reference", SemanticFrame(None, "Reference", "Reference"))
        }
        slots["reference"].semantic_frame.utterance = "today"
        semantic_object = SemanticFrame(None, "Date", "DateByReference", slots)
        da = DiscourseAnalysis()

        # act
        da._bind_date(semantic_object)
