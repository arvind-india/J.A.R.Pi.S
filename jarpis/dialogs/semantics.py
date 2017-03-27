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
    entity_type = "User"

    @classmethod
    def bind(cls, frame, user):
        if frame.entity_type == cls.entity_type:
            username_frame = SemanticFrame(None, "Username", "Username")
            username_frame.utterance = frame.slots["reference"].utterance
            username_frame.value = user.name
            slots = {
                "name": Slot(cls.entity_type, "name", username_frame)
            }

            user_frame = cls(frame.grammar, cls.entity_type,
                             cls.entity_type, slots)
            user_frame.entity = user
            return user_frame
        else:
            raise ValueError(("Entity type of semantic frame does not match"
                              "expected type. (actual={0} | expected={1}").format(frame.entity_type, cls.entity_type))


class SemanticDateFrame(SemanticFrame):
    entity_type = "Date"

    @classmethod
    def bind(cls, frame, date):
        if frame.entity_type == cls.entity_type:
            timestamp_frame = SemanticFrame(None, "Timestamp", "Timestamp")
            timestamp_frame.utterance = frame.slots["reference"].utterance
            timestamp_frame.value = date.isoformat()
            slots = {
                "timestamp": Slot(cls.entity_type, "timestamp", timestamp_frame)
            }

            date_frame = cls(frame.grammar, cls.entity_type,
                             cls.entity_type, slots)
            date_frame.entity = date
            return date_frame
        else:
            raise ValueError(("Entity type of semantic frame does not match"
                              "expected type. (actual={0} | expected={1}").format(frame.entity_type, cls.entity_type))
