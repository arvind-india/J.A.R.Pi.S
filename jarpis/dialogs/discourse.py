import jarpis.recognition.speakerRecognition as speakerRecognition
from jarpis.user import User, UserNotFoundException
from jarpis.calendar import Calendar
from jarpis.dialogs.semantics import SemanticUserFrame, SemanticDateFrame


class DiscourseAnalysis:

    def __init__(self, event_mediator):
        self._communication = event_mediator
        self._register_events()

    def _register_events(self):
        self._communication.register(
            "evaluationRequest", self._evaluate)

    def _evaluate(self, semantic_object):
        entity_type = semantic_object.entity_type

        if entity_type == "User":
            self._bind_user(semantic_object)
        if entity_type == "Date":
            self._bind_date(semantic_object)
        if entity_type == "Period":
            self._bind_period(semantic_object)
        if entity_type == "Query":
            '''
            If I'm correct then every query can be instantly evaluated.
            There is no binding necessary and the "events" and "items"
            lists should be filled by the action performed afterwards by
            the dialog manager
            '''
            self._communication.publish(
                "evaluationSuccessful", semantic_object)

    def _bind_user(self, semantic_object):
        semantic_class = semantic_object.semantic_class
        if semantic_class == "UserByReference":
            # this means the user said something with a self reference like:
            # "for me, my, I"
            speaker = speakerRecognition.get_current_speaker()

            if speaker[0] == "anonymous":
                self._communication.publish(
                    "evaluationFailed", semantic_object)
                return

            try:
                user = User.getUserFromSpeaker(speaker)
            except UserNotFoundException:
                self._communication.publish(
                    "invalidInformation", semantic_object)
                return

            bound_object = SemanticUserFrame.bind(semantic_object, user)
            self._communication.publish("evaluationSuccessful", bound_object)
        else:
            raise ValueError(
                "Unknown semantic class '{0}'".format(semantic_class))

    def _bind_date(self, semantic_object):
        semantic_class = semantic_object.semantic_class
        if semantic_class == "DateByReference":
            reference = semantic_object["reference"].utterance
            possible_references = {
                "yesterday": -1,
                "today": 0,
                "tomorrow": 1,
            }

            if reference not in possible_references:
                self._communication.publish(
                    "invalidInformation", semantic_object)
                return

            offset_in_days = possible_references[reference]
            today = Calendar.getCurrentDate()
            target_date = Calendar.getDateByOffset(today, offset_in_days)
            bound_object = SemanticDateFrame.bind(semantic_object, target_date)
            self._communication.publish("evaluationSuccessful", bound_object)
        elif semantic_class == "DateByDays":
            offset_in_days = semantic_object["days"].utterance
            today = Calendar.getCurrentDate()
            target_date = Calendar.getDateByOffset(today, offset_in_days)
            bound_object = SemanticDateFrame.bind(semantic_object, target_date)
            self._communication.publish("evaluationSuccessful", bound_object)
        elif semantic_class == "DateByComponents":
            day = semantic_object["day"].utterance
            month = semantic_object["month"].utterance
            year = semantic_object["year"].utterance

            try:
                target_date = Calendar.getDateFor(
                    day=day, month=month, year=year)
            except ValueError:
                self._communication.publish(
                    "invalidInformation", semantic_object)
                return

            bound_object = SemanticDateFrame.bind(semantic_object, target_date)
            self._communication.publish("evaluationSuccessful", bound_object)

    def _bind_period(self, semantic_object):
        semantic_class = semantic_object.semantic_class
        if semantic_class == "Period":
            start_date = semantic_object["start"].value
            end_date = semantic_object["end"].value

            if start_date is None or end_date is None:
                self._communication.publish(
                    "evaluationFailed", semantic_object)
                return

            if start_date > end_date:
                self._communication.publish(
                    "evaluationFailed", semantic_object)
                return

            current = Calendar.getCurrentDate()
            if start_date < current or end_date < current:
                self._communication.publish(
                    "evaluationFailed", semantic_object)
                return

            self._communication.publish("evaluationSuccessful", bound_object)
