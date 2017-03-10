from __future__ import absolute_import

import unittest
from jarpis.dialogs.discourse import DiscourseUnit, DiscourseTree
from jarpis.dialogs.semantics import SemanticClass


class A_semantic_object_can_be_correctly_inserted_into_a_discourse_tree(unittest.TestCase):

    def test_if_the_appropriate_discourse_unit_is_the_tree_root(self):
        # arrange
        leaf_nodes = [DiscourseUnit(None, "InappropriateType1")]
        root_children = [DiscourseUnit(None, "InappropriateType2", leaf_nodes)]
        root = DiscourseUnit(None, "AppropriateType", root_children)
        discourse_tree = DiscourseTree(root)
        object_to_insert = SemanticClass(None, "AppropriateType")

        target_unit = root

        # act
        discourse_tree.insert(object_to_insert)

        # assert
        self.assertTrue(leaf_nodes[0].is_empty)
        self.assertTrue(root_children[0].is_empty)
        self.assertFalse(target_unit.is_empty)
        self.assertIs(target_unit.semantic_object, object_to_insert)

    def test_if_the_appropriate_discourse_unit_is_an_inner_node(self):
        # arrange
        leaf_nodes = [DiscourseUnit(None, "InappropriateType1")]
        root_children = [DiscourseUnit(None, "AppropriateType", leaf_nodes)]
        root = DiscourseUnit(None, "InappropriateType2", root_children)
        discourse_tree = DiscourseTree(root)
        object_to_insert = SemanticClass(None, "AppropriateType")

        target_unit = root_children[0]

        # act
        discourse_tree.insert(object_to_insert)

        # assert
        self.assertTrue(leaf_nodes[0].is_empty)
        self.assertTrue(root.is_empty)
        self.assertFalse(target_unit.is_empty)
        self.assertIs(target_unit.semantic_object, object_to_insert)

    def test_if_the_appropriate_discourse_unit_is_a_leaf(self):
        # arrange
        leaf_nodes = [DiscourseUnit(None, "AppropriateType")]
        root_children = [DiscourseUnit(None, "InappropriateType1", leaf_nodes)]
        root = DiscourseUnit(None, "InappropriateType2", root_children)
        discourse_tree = DiscourseTree(root)
        object_to_insert = SemanticClass(None, "AppropriateType")

        target_unit = leaf_nodes[0]

        # act
        discourse_tree.insert(object_to_insert)

        # assert
        self.assertTrue(root.is_empty)
        self.assertTrue(root_children[0].is_empty)
        self.assertFalse(target_unit.is_empty)
        self.assertIs(target_unit.semantic_object, object_to_insert)
