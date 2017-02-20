from parsetron import Grammar, RobustParser


def interpret(self, utterance):
    def semanticObjectFrom(parseResult):
        pass

    parser = RobustParser(SemanticClass(None).grammar)
    tree, result = parser.parse(utterance)

    return semanticObjectFrom(result)


class SemanticClass:
    def __init__(self, grammar, type, slots=None):
        if slots is None:
            slots = []

        self._grammar = grammar
        self._type = type
        self._slots = slots


class Slot:
    def __init__(self, type, name):
        self._type = type
        self._name = name
