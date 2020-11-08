from unittest import TestCase
import os
from ppdp_anonops.utils import *


class Test_Utils_TaxonomyTree(TestCase):

    def test_CreateTree(self):
        tax = TaxonomyTree()
        n_healthcare = tax.addNode("Healthcare")
        n_aerospace = tax.addNode("Aerospace")
        n_it = tax.addNode("IT")

        self.assertIsNotNone(n_healthcare)
        self.assertIsNotNone(n_aerospace)
        self.assertIsNotNone(n_it)

        self.assertEqual(len(tax.RootNode.Children), 3)

    def test_SearchTree(self):
        pass

    def test_TreeAsDictByLevel(self):
        pass
