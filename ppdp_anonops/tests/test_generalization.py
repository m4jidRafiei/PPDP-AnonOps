from unittest import TestCase
import os
from ppdp_anonops import Generalization
from ppdp_anonops.utils import TaxonomyTree, TaxonomyTreeNode


class TestGeneralization(TestCase):
    def getTestXesPath(self):
        return os.path.join(os.path.dirname(__file__), 'resources', 'running_example.xes')

    def test_01_generalizationTime(self):
        s = Generalization(self.getTestXesPath())

        no_events = sum([len(trace) for trace in s.xesLog])

        s.GeneralizeEventTimeAttribute("time:timestamp", "seconds")
        self.assertEqual(self.getTime(s.xesLog, "time:timestamp", "seconds"), 0)

        s.GeneralizeEventTimeAttribute("time:timestamp", "minutes")
        self.assertEqual(self.getTime(s.xesLog, "time:timestamp", "minutes"), 0)

        s.GeneralizeEventTimeAttribute("time:timestamp", "hours")
        self.assertEqual(self.getTime(s.xesLog, "time:timestamp", "hours"), 0)

        s.GeneralizeEventTimeAttribute("time:timestamp", "days")
        self.assertEqual(self.getTime(s.xesLog, "time:timestamp", "days"), 0)

        s.GeneralizeEventTimeAttribute("time:timestamp", "months")
        self.assertEqual(self.getTime(s.xesLog, "time:timestamp", "months"), no_events)  # no_events as default value for days is 1 and not 0 (0 is an ivalid day-of-month)

    def test_02_generalizationResourceTaxonomy(self):
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
        n_it = n_insurance.AddChildNode("IT")
        n_insurance.AddChildNode("Consulting")
        n_support = n_insurance.AddChildNode("Support")
        n_it.AddChildNode("Ellen")
        n_it.AddChildNode("Mike")
        n_it.AddChildNode("Pete")
        n_support.AddChildNode("Sara")
        n_support.AddChildNode("Sean")
        n_support.AddChildNode("Sue")

        n_aerospace = tax.AddNode("Aerospace")
        n_it = tax.AddNode("IT")

        s = Generalization(self.getTestXesPath())

        bCountIT = 0
        bCountSupport = 0
        for case_index, case in enumerate(s.xesLog):
            for event_index, event in enumerate(case):
                if event["org:resource"] in ["Ellen", "Mike", "Pete"]:
                    bCountIT += 1
                elif event["org:resource"] in ["Sara", "Sean", "Sue"]:
                    bCountSupport += 1

        s.GeneralizeEventAttributeByTaxonomyTreeDepth("org:resource", tax, 3)

        aCountIT = 0
        aCountSupport = 0
        for case_index, case in enumerate(s.xesLog):
            for event_index, event in enumerate(case):
                if event["org:resource"] == "IT":
                    aCountIT += 1
                elif event["org:resource"] == "Support":
                    aCountSupport += 1

        self.assertEqual(aCountIT, bCountIT, "Before and After count of resources expected does not match")
        self.assertEqual(aCountSupport, bCountSupport, "Before and After count of resources expected does not match")

        # Test again with higher level of generalization
        s = Generalization(self.getTestXesPath())
        s.GeneralizeEventAttributeByTaxonomyTreeDepth("org:resource", tax, 2)

        aCountInsurance = 0
        for case_index, case in enumerate(s.xesLog):
            for event_index, event in enumerate(case):
                if event["org:resource"] == "Insurance":
                    aCountInsurance += 1

        self.assertEqual(aCountIT + aCountSupport, aCountInsurance, "Before and After count of resources expected does not match")

    def getTime(self, xesLog, dateTimeAttribute, generalizationLevel):
        ret = 0

        for case_index, case in enumerate(xesLog):
            for event_index, event in enumerate(case):
                if(generalizationLevel == "seconds"):
                    ret += event[dateTimeAttribute].microsecond

                if(generalizationLevel == "minutes"):
                    ret += event[dateTimeAttribute].second

                if(generalizationLevel == "hours"):
                    ret += event[dateTimeAttribute].minute

                if(generalizationLevel == "days"):
                    ret += event[dateTimeAttribute].hour

                if(generalizationLevel == "months"):
                    ret += event[dateTimeAttribute].day

                if(generalizationLevel == "years"):
                    ret += event[dateTimeAttribute].month
        return ret
