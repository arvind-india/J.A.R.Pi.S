import jarpis.dialogs
from jarpis.user import User, UserNotFoundException
from jarpis.dialogs.semantics import SemanticClass


class DiscourseAnalysis:

    def __init__(self):
        self._register_events()

    def _register_events(self):
        jarpis.dialogs.communication.register(
            "evaluationRequest", self._evalute)

    def _evaluate(self, semantic_object):
        entity_type = semantic_object.entity_type
        if entity_type == "User":
            self._bind_user(semantic_object)

    def _bind_user(self, semantic_object):
        semantic_class = semantic_object.semantic_class
        if semantic_class == "UserByReference":
            # this means the user said something with a self reference like:
            # "for me, my, I"
            # -> get the user from the speaker recognition
            speaker = None
            try:
                user = User.getUserFromSpeaker(speaker)
            except UserNotFoundException:
                # no user for speaker! publish error
                return

            # TODO either fill a dict or have SemanticClass subclass for each
            # entity
            bound_object = semantic_object.bind({})
            bound_object.entity = user
            jarpis.dialogs.communication.publish(
                "evaluationSuccessful", bound_object)
