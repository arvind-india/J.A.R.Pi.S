from __future__ import absolute_import
import unittest
from parsetron import Grammar, Set, Regex, Optional
from jarpis.dialogs.semantics import SemanticInterpreter, SemanticClass, Slot


class An_utterance_can_be_parsed_into_a_semantic_class_correctly(unittest.TestCase):
    def setUp(self):
        class TestGrammar(Grammar):
            language = Set(["Java", "JavaScript", "Python", "C#"])
            no = Regex("not")
            adjective = Set(["cool", "fun", "horrible"])

            utterance = language + "is" + Optional(no) + adjective
            GOAL = utterance

        self._grammar = TestGrammar()

    def tearDown(self):
        del self._grammar

    def if_it_contains_the_necessary_keywords(self):
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
