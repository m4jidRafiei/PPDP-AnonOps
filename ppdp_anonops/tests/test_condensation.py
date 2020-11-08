from unittest import TestCase
import os
from ppdp_anonops import Condensation


class TestCondensation(TestCase):
    def getTestXesPath(self):
        return os.path.join(os.path.dirname(__file__), 'resources', 'Sepsis Cases - Event Log.xes')

    def test_eventLevelCondensation(self):
        for clusters in range(4, 7):
            s = Condensation(self.getTestXesPath())

            # Needs to be a numeric attribute
            matchAttribute = "CRP"

            s.CondenseEventAttributeBykMeanClusterMode(matchAttribute, clusters)

            self.assertEqual(self.__getNumberOfDistinctEventAttributeValues(s, matchAttribute), clusters)

    def __getNumberOfDistinctEventAttributeValues(self, s, attribute):
        values = []

        for case_index, case in enumerate(s.xesLog):
            for event_index, event in enumerate(case):
                if(attribute in event.keys() and event[attribute] not in values):
                    values.append(event[attribute])

        return len(values)
