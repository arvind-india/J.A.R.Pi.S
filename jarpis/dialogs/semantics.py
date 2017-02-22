from parsetron import RobustParser


class SemanticInterpreter:
    def __init__(self, semantic_classes=None):
        if semantic_classes is None:
            semantic_classes = []
        self._semantic_classes = semantic_classes

    def interpret(self, utterance):
        if utterance is None:
            return None
        if not utterance.strip():
            return None

        for semantic_class in self._semantic_classes:
            parser = RobustParser(semantic_class.grammar)
            tree, result = parser.parse(utterance)
            if tree is not None:
                return semantic_class.fill_slots(result)

        return None


class SemanticClass:
    def __init__(self, grammar, type, slots=None):
        if slots is None:
            slots = {}

        self._grammar = grammar
        self._type = type
        self._slots = slots

    @property
    def grammar(self):
        return self._grammar

    @property
    def slots(self):
        return self._slots

    def fill_slots(self, parse_results):
        for name, slot in self._slots.iteritems():
            parsed_value = parse_results[name]
            if parsed_value is not None:
                slot.value = parsed_value

        return self


class Slot:
    def __init__(self, type, name):
        self._type = type
        self._name = name
        self._value = None

    def __repr__(self):
        return "name=%s, type=%s, value=%s" % (self.name, self.type, self.value)

    @property
    def value(self):
        return self._value

    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return self._type

    @value.setter
    def value(self, value):
        if value is not None:
            self._value = value
