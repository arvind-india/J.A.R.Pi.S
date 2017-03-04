from __future__ import absolute_import
import unittest
from mock import Mock
from parsetron import Grammar, Set
import jarpis.dialogs
from jarpis.dialogs.semantics import SemanticInterpreter, SemanticClass, Slot


class The_interpreter_can_instantiate_a_semantic_object(unittest.TestCase):

    def setUp(self):
        class TestGrammar(Grammar):
            language = Set(["Java", "JavaScript", "Python", "C#"])
            adjective = Set(["cool", "fun", "horrible"])

            utterance = language + adjective
            GOAL = utterance

        self._grammar = TestGrammar()
        self._communication = jarpis.dialogs.communication

    def tearDown(self):
        del self._grammar
        del self._communication

    def test_if_the_utterance_contains_the_necessary_keywords(self):
        # arrange
        slots = {"language": Slot(None, "language"),
                 "adjective": Slot(None, "adjective")}
        semantic_class = SemanticClass(self._grammar, "test", slots)
        interpreter = SemanticInterpreter([semantic_class])
        utterance = "Python is cool"

        def handler(semantic_object):
            # assertions
            self.assertIn("language", semantic_object.slots)
            self.assertIn("adjective", semantic_object.slots)
            self.assertEqual(semantic_object.slots["language"].value, "Python")
            self.assertEqual(semantic_object.slots["adjective"].value, "cool")

        handlerMock = Mock(wraps=handler)

        self._communication.register(
            "interpretationSuccessfull", handlerMock)

        # act
        interpreter.interpret(utterance)

        # assert
        handlerMock.assert_called_once()


class The_interpreter_can_not_instantiate_a_semantic_object(unittest.TestCase):

    def setUp(self):
        class TestGrammar(Grammar):
            language = Set(["Java", "JavaScript", "Python", "C#"])
            adjective = Set(["cool", "fun", "horrible"])

            utterance = language + adjective
            GOAL = utterance

        self._grammar = TestGrammar()
        self._communication = jarpis.dialogs.communication

    def tearDown(self):
        del self._grammar
        del self._communication

    def test_if_the_utterance_does_not_contain_the_necessary_keywords(self):
        # arrange
        slots = {"language": Slot(None, "language"),
                 "adjective": Slot(None, "adjective")}
        semantic_class = SemanticClass(self._grammar, "test", slots)
        interpreter = SemanticInterpreter([semantic_class])
        utterance = "Dodo ist ein Chefkoch"
        interpretationSuccessfull = Mock()
        interpretationFinished = Mock()
        self._communication.register(
            "interpretationSuccessfull", interpretationSuccessfull)
        self._communication.register(
            "interpretationFinished", interpretationFinished)

        # act
        interpreter.interpret(utterance)

        # assert
        interpretationSuccessfull.assert_not_called()
        interpretationFinished.assert_called_once()

    def test_if_the_utterance_is_empty(self):
        # arrange
        slots = {"language": Slot(None, "language"),
                 "adjective": Slot(None, "adjective")}
        semantic_class = SemanticClass(self._grammar, "test", slots)
        interpreter = SemanticInterpreter([semantic_class])
        utterance = ""
        handler = Mock()
        self._communication.register("nothingToInterpret", handler)

        # act
        interpreter.interpret(utterance)

        # assert
        handler.assert_called_once()

    def test_if_the_utterance_is_None(self):
        # arrange
        slots = {"language": Slot(None, "language"),
                 "adjective": Slot(None, "adjective")}
        semantic_class = SemanticClass(self._grammar, "test", slots)
        interpreter = SemanticInterpreter([semantic_class])
        utterance = None
        handler = Mock()
        self._communication.register("nothingToInterpret", handler)

        # act
        interpreter.interpret(utterance)

        # assert
        handler.assert_called_once()
