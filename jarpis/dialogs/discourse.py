import jarpis.dialogs
import jarpis.recognition.speakerRecognition as speakerRecognition
from jarpis.user import User, UserNotFoundException
from jarpis.calendar import Calendar
from jarpis.dialogs.semantics import SemanticUserFrame, SemanticDateFrame


class DiscourseAnalysis:

    def __init__(self):
        self._register_events()

    def _register_events(self):
        jarpis.dialogs.communication.register(
            "evaluationRequest", self._evaluate)

    def _evaluate(self, semantic_object):
        entity_type = semantic_object.entity_type
        if entity_type == "User":
            self._bind_user(semantic_object)
        if entity_type == "Date":
            self._bind_date(semantic_object)

    def _bind_user(self, semantic_object):
        communication = jarpis.dialogs.communication
        semantic_class = semantic_object.semantic_class
        if semantic_class == "UserByReference":
            # this means the user said something with a self reference like:
            # "for me, my, I"
            speaker = speakerRecognition.get_current_speaker()

            if speaker[0] == "anonymous":
                communication.publish("evaluationFailed", semantic_object)
                return

            try:
                user = User.getUserFromSpeaker(speaker)
            except UserNotFoundException:
                communication.publish("invalidInformation", semantic_object)
                return

            bound_object = SemanticUserFrame.bind(semantic_object, user)
            communication.publish("evaluationSuccessful", bound_object)
        else:
            raise ValueError(
                "Unknown semantic class '{0}'".format(semantic_class))

    def _bind_date(self, semantic_object):
        communication = jarpis.dialogs.communication
        semantic_class = semantic_object.semantic_class
        if semantic_class == "DateByReference":
            reference = semantic_object.utterance
            possible_references = {
                "yesterday": -1,
                "today": 0,
                "tomorrow": 1,
            }

            if reference not in possible_references:
                communication.publish("invalidInformation", semantic_object)
                return

            offset_in_days = possible_references[reference]
            today = Calendar.getCurrentDate()
            target_date = Calendar.getDateByOffset(today, offset_in_days)
            bound_object = SemanticDateFrame.bind(semantic_object, target_date)
            communication.publish("evaluationSuccessful", bound_object)
