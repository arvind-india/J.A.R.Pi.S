import jarpis.dialogs


class DialogManager:

    def __init__(self):
        self._register_events()

    def _register_events(self):
        # semantic interpreter events
        jarpis.dialogs.communication.register(
            "interpretationSuccessfull", self._insert_in_discourse_tree)
        jarpis.dialogs.communication.register(
            "nothingToInterpret", self._nothing_to_interpret)
        jarpis.dialogs.communication.register(
            "interpretationFinished", self._start_semantic_evaluation)

        # discourse analysis events
        jarpis.dialogs.communication.register(
            "evaluationSuccessfull", self._semantic_object_evaluated)
        jarpis.dialogs.communication.register(
            "evaluationFailed", self._semantic_object_evaluation_failed)
        jarpis.dialogs.communication.register(
            "invalidInformation", self._invalid_semantic_object_information)

    def _insert_in_discourse_tree(self, semantic_object):
        pass

    def _start_semantic_evaluation(self):
        pass

    def _nothin_to_interpret(self):
        pass

    def _semantic_object_evaluated(self, semantic_object):
        pass

    def _semantic_object_evaluation_failed(self, semantic_object):
        pass

    def _invalid_semantic_object_information(self, semantic_object):
        pass


class DiscourseUnit:

    def __init__(self, evaluation_strategy, entity_type, children):
        self._evaluation_strategy = evaluation_strategy
        self._is_resolved = False
        self._type = entity_type
        self._children = children
        self._semantic_object = None

    def resolve(self):
        self._is_resolved = True

    @property
    def _is_resolved(self):
        return self._is_resolved

    @property
    def semantic_object(self):
        return self._semantic_object

    @semantic_object.setter
    def semantic_object(self, value):
        self._semantic_object = value


class DiscourseTree:
    pass


class SemanticEvaluationError(Exception):
    pass
