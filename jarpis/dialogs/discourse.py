import jarpis.dialogs


class DialogManager:

    def __init__(self):
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
