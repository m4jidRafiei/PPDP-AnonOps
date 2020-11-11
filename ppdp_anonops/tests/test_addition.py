from unittest import TestCase
import os
from ppdp_anonops import Addition
from pm4py.objects.log.importer.xes import factory as xes_importer


class TestAddition(TestCase):
    def getTestXesLog(self):
        xesPath = os.path.join(os.path.dirname(__file__), 'resources', 'running_example.xes')
        return xes_importer.apply(xesPath)

    def test_additionEventAtTraceEnd(self):
        log = self.getTestXesLog()

        s = Addition()

        matchAttribute = "org:resource"
        matchAttributeValue = "Ellen"

        no_traces = len(log)
        no_events = sum([len(trace) for trace in log])
        self.assertEqual(no_traces, 6)
        self.assertEqual(no_events, 42)

        log = s.AddEvent(log, matchAttribute, matchAttributeValue)

        no_traces = len(log)
        no_events = sum([len(trace) for trace in log])
        self.assertEqual(no_traces, 6)
        self.assertEqual(no_events, 45)
