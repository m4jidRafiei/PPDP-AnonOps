from unittest import TestCase
import os
from ppdp_anonops.utils import *
import logging
import sys


class Test_Utils_TaxonomyTree(TestCase):
    def _generateTestTree(self):
        tax = TaxonomyTree()
        n_healthcare = tax.AddNode("Healthcare")

        n_hospital = n_healthcare.AddChildNode("Hospital")
        n_surgery = n_hospital.AddChildNode("Surgery")
        n_surgery.AddChildNode("Surgeon")
        n_surgery.AddChildNode("Anesthesist")
        n_surgery.AddChildNode("Caretaker")
        n_diagnostic = n_hospital.AddChildNode("Diagnostic")
        n_diagnostic.AddChildNode("Internist")
        n_diagnostic.AddChildNode("Pharmacist")
        n_diagnostic.AddChildNode("Caretaker")

        n_insurance = n_healthcare.AddChildNode("Insurance")
        n_insurance.AddChildNode("Bookkeeping")
        n_insurance.AddChildNode("IT")
        n_insurance.AddChildNode("Consulting")
        n_insurance.AddChildNode("Support")

        n_aerospace = tax.AddNode("Aerospace")
        n_it = tax.AddNode("IT")

        return tax

    def test_01_CreateTree(self):
        tax = self._generateTestTree()
        self.assertEqual(len(tax.RootNode.Children), 3)

    def test_02_SearchTree(self):
        tax = self._generateTestTree()
        self.assertFalse(True, 'IMPLEMENT SEARCH OPERATIONS!')
        pass

    def test_03_ImportTree(self):
        tax = self._generateTestTree()
        self.assertFalse(True, 'IMPLEMENT IMPORT/EXPORT OPERATIONS!')
        pass

    def test_04_TreeAsDictByLevel(self):
        tax = self._generateTestTree()

        # All nodes below level 2 get generalized to level 2 names
        dict = tax.GetGeneralizedDict_NodeNameToLevelXParentalName(2)
        for n in ['Surgeon', 'Anesthesist', 'Caretaker', 'Surgery', 'Internist', 'Pharmacist', 'Diagnostic']:
            self.assertTrue(n in dict.keys() and dict[n] == 'Hospital')
        for n in ['Bookkeeping', 'IT', 'Consulting', 'Support']:
            self.assertTrue(n in dict.keys() and dict[n] == 'Insurance')

        # All nodes below level 3 get generalized to level 3 names
        dict = tax.GetGeneralizedDict_NodeNameToLevelXParentalName(3)
        for n in ['Surgeon', 'Anesthesist']:
            self.assertTrue(n in dict.keys() and dict[n] == 'Surgery')
        for n in ['Caretaker', 'Internist', 'Pharmacist']:
            self.assertTrue(n in dict.keys() and dict[n] == 'Diagnostic')

        # As there are nodes on depth 4, but no nodes below them, the result should be empty
        dict = tax.GetGeneralizedDict_NodeNameToLevelXParentalName(4)
        self.assertEqual(len(dict.keys()), 0)
        pass
