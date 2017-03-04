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

    def evaluate(self):
        '''
        TODO when is a discourse unit considered to be evaluated?
        the tree should collapse upwards and children should be removed from
        their parent. If the root node has no children it is considered to be
        evaluated and can be semantically bound to the domain object
        '''
        for child_unit in self._children:
            if not child_unit._is_resolved:
                child_unit.evaluate()

        if self.semantic_object is not None:
            jarpis.dialogs.communication.publish(
                "requestEvaluation", self.semantic_object)
        else:
            raise SemanticEvaluationError(
                "Cannot evaluate semantic object that is None.")

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
