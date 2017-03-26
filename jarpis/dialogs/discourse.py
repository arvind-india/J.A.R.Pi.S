import jarpis.dialogs


class DiscourseAnalysis:

    def __init__(self):
        self._register_events()

    def _register_events(self):
        jarpis.dialogs.communication.register(
            "evaluationRequest", self._evalute)

    def _evaluate(self, semantic_object):
        pass
