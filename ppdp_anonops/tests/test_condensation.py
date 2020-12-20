from unittest import TestCase
import os
from ppdp_anonops import Condensation
from pm4py.objects.log.importer.xes import factory as xes_importer


class TestCondensation(TestCase):
    def getTestXesLog(self):
        xesPath = os.path.join(os.path.dirname(__file__), 'resources', 'Sepsis Cases - Event Log.xes')
        return xes_importer.apply(xesPath)

    def test_01_eventLevelCondensation(self):
        for clusters in range(4, 7):
            log = self.getTestXesLog()

            s = Condensation()

            # Needs to be a numeric attribute
            matchAttribute = "CRP"

            log = s.CondenseEventAttributeBykMeanCluster(log, matchAttribute, ["org:group"], clusters, "mode")

            self.assertEqual(self.__getNumberOfDistinctEventAttributeValues(log, matchAttribute), clusters)

    def test_02_eee(self):
        log = xes_importer.apply(os.path.join(os.path.dirname(__file__), 'resources', 'running_exampleWithCostsAsInt.xes'))
        s = Condensation()

        # Needs to be a numeric attribute
        matchAttribute = "Costs"

        log = s.CondenseEventAttributeBykMeanCluster(log, matchAttribute, ["Activity", "Resource"], 4, "mean")

        self.assertEqual(self.__getNumberOfDistinctEventAttributeValues(log, matchAttribute), 4)

    def __getNumberOfDistinctEventAttributeValues(self, xesLog, attribute):
        values = []

        for case_index, case in enumerate(xesLog):
            for event_index, event in enumerate(case):
                if(attribute in event.keys() and event[attribute] not in values):
                    values.append(event[attribute])

        return len(values)
