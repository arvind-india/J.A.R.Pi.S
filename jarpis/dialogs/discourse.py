import jarpis.dialogs
import jarpis.recognition.speakerRecognition as speakerRecognition
from jarpis.user import User, UserNotFoundException
from jarpis.dialogs.semantics import SemanticUserFrame


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
            bound_object.entity = user
            communication.publish("evaluationSuccessful", bound_object)
        else:
            raise ValueError(
                "Unknown semantic class '{0}'".format(semantic_class))
