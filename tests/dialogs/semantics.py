from __future__ import absolute_import
import unittest
from parsetron import Grammar, Set, Regex, Optional
from jarpis.dialogs.semantics import SemanticInterpreter, SemanticClass, Slot


class The_interpreter_can_instantiate_a_semantic_object(unittest.TestCase):
    def setUp(self):
        class TestGrammar(Grammar):
            language = Set(["Java", "JavaScript", "Python", "C#"])
            adjective = Set(["cool", "fun", "horrible"])

            utterance = language + adjective
            GOAL = utterance

        self._grammar = TestGrammar()

    def tearDown(self):
        del self._grammar

    def test_if_the_utterance_contains_the_necessary_keywords(self):
        # arrange
        slots = {"language": Slot(None, "language"), "adjective": Slot(None, "adjective")}
        semantic_class = SemanticClass(self._grammar, "test", slots)
        interpreter = SemanticInterpreter([semantic_class])
        utterance = "Python is cool"

        # act
        semantic_object = interpreter.interpret(utterance)

        # assert
        self.assertIn("language", semantic_object.slots)
        self.assertIn("adjective", semantic_object.slots)
        self.assertEqual(semantic_object.slots["language"].value, "Python")
        self.assertEqual(semantic_object.slots["adjective"].value, "cool")


class The_interpreter_can_not_instantiate_a_semantic_object(unittest.TestCase):
    def setUp(self):
        class TestGrammar(Grammar):
            language = Set(["Java", "JavaScript", "Python", "C#"])
            adjective = Set(["cool", "fun", "horrible"])

            utterance = language + adjective
            GOAL = utterance

        self._grammar = TestGrammar()

    def tearDown(self):
        del self._grammar

    def test_if_the_utterance_does_not_contain_the_necessary_keywords(self):
        # arrange
        slots = {"language": Slot(None, "language"),
                 "adjective": Slot(None, "adjective")}
        semantic_class = SemanticClass(self._grammar, "test", slots)
        interpreter = SemanticInterpreter([semantic_class])
        utterance = "Dodo ist ein Chefkoch"

        # act
        semantic_object = interpreter.interpret(utterance)

        # assert
        self.assertIsNone(semantic_object)

    def test_if_the_utterance_is_empty(self):
        # arrange
        slots = {"language": Slot(None, "language"),
                 "adjective": Slot(None, "adjective")}
        semantic_class = SemanticClass(self._grammar, "test", slots)
        interpreter = SemanticInterpreter([semantic_class])
        utterance = ""

        # act
        semantic_object = interpreter.interpret(utterance)

        # assert
        self.assertIsNone(semantic_object)

    def test_if_the_utterance_is_None(self):
        # arrange
        slots = {"language": Slot(None, "language"),
                 "adjective": Slot(None, "adjective")}
        semantic_class = SemanticClass(self._grammar, "test", slots)
        interpreter = SemanticInterpreter([semantic_class])
        utterance = None

        # act
        semantic_object = interpreter.interpret(utterance)

        # assert
        self.assertIsNone(semantic_object)
