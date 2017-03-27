from semantics import SemanticInterpreter
from events import EventMediator

communication = EventMediator()
semantic_interpreter = SemanticInterpreter(communication, [])
