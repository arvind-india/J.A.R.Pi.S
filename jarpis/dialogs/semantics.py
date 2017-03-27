from parsetron import RobustParser
import jarpis.dialogs


class SemanticInterpreter:

    def __init__(self, semantic_classes=None):
        if semantic_classes is None:
            semantic_classes = []
        self._semantic_classes = semantic_classes

    def interpret(self, utterance):
        communication = jarpis.dialogs.communication

        if utterance is None or not utterance.strip():
            communication.publish("nothingToInterpret")
            return

        for semantic_class in self._semantic_classes:
            parser = RobustParser(semantic_class.grammar)
            tree, result = parser.parse(utterance)
            if tree is not None:
                communication.publish(
                    "interpretationSuccessful",
                    semantic_class.fill_slots(result))

        # TODO Do we need to explicitly publish an event if no semantic object could be parsed?
        # Need a boolean then to check if any semantic object could be parsed.
        communication.publish("interpretationFinished")


class SemanticFrame:

    def __init__(self, grammar, type, semantic_class, slots=None):
        if slots is None:
            slots = {}

        self._grammar = grammar
        self._type = type
        self._class = semantic_class
        self._slots = slots

    @property
    def entity_type(self):
        return self._type

    @property
    def grammar(self):
        return self._grammar

    @property
    def semantic_class(self):
        return self._class

    @property
    def utterance(self):
        return self._utterance

    @utterance.setter
    def utterance(self, value):
        if value is not None:
            self._utterance = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if value is not None:
            self._value = value

    @property
    def slots(self):
        return self._slots

    def fill_slots(self, parse_results):
        for name, slot in self._slots.iteritems():
            parsed_value = parse_results[name]
            if parsed_value is not None:
                slot.semantic_frame.utterance = parsed_value

        return self


class Slot:

    def __init__(self, type, name, semantic_frame):
        self._type = type
        self._name = name
        self.semantic_frame = semantic_frame

    def __repr__(self):
        return ("name=%s, type=%s, value=%s" %
                (self.name, self.type, self.semantic_frame))

    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return self._type

    @property
    def utterance(self):
        return self.semantic_frame.utterance

    @property
    def value(self):
        return self.semantic_frame.value


class SemanticUserFrame(SemanticFrame):

    @classmethod
    def bind(cls, frame, user):
        if frame.entity_type == "User":
            username_frame = SemanticFrame(None, "Username", "Username")
            username_frame.utterance = frame.slots["reference"].utterance
            username_frame.value = user.name
            slots = {
                "name": Slot("User", "name", username_frame)
            }

        return cls(frame.grammar, frame.entity_type, "User", slots)


class SemanticDateFrame(SemanticFrame):

    def bind(cls, frame, date):
        slots = {}
