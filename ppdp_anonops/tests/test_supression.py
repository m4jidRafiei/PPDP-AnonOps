from unittest import TestCase
import os
from ppdp_anonops import Supression


class TestSupression(TestCase):
    def getTestXesPath(self):
        return os.path.join(os.path.dirname(__file__), 'resources', 'running_example.xes')

    def test_suppressEvent(self):
        s = Supression(self.getTestXesPath())

        no_traces = len(s.xesLog)
        no_events = sum([len(trace) for trace in s.xesLog])
        self.assertEqual(no_traces, 6)
        self.assertEqual(no_events, 42)

        s.SuppressEvent("concept:name", "reinitiate request")  # concept:name is activity

        no_traces = len(s.xesLog)
        no_events = sum([len(trace) for trace in s.xesLog])
        self.assertEqual(no_traces, 6)
        self.assertEqual(no_events, 39)

    def test_suppressEventAttribute(self):
        s = Supression(self.getTestXesPath())

        matchAttribute = "concept:name"
        matchAttributeValue = "reinitiate request"
        supressedAttribute = "org:resource"

        no_traces = len(s.xesLog)
        no_events = sum([len(trace) for trace in s.xesLog])
        counter = 0

        for case_index, case in enumerate(s.xesLog):
            for event_index, event in enumerate(case):
                if (event[matchAttribute] == matchAttributeValue):
                    if(event[supressedAttribute] == None):
                        counter += 1

        self.assertEqual(no_traces, 6)
        self.assertEqual(no_events, 42)
        self.assertEqual(counter, 0)

        # Supress resource if activity matches 'reinitiate request'
        s.SuppressEventAttribute("concept:name", "reinitiate request", "org:resource")

        no_traces = len(s.xesLog)
        no_events = sum([len(trace) for trace in s.xesLog])
        counter = 0

        for case_index, case in enumerate(s.xesLog):
            for event_index, event in enumerate(case):
                if (event[matchAttribute] == matchAttributeValue):
                    if(event[supressedAttribute] == None):
                        counter += 1

        self.assertEqual(no_traces, 6)
        self.assertEqual(no_events, 42)
        self.assertEqual(counter, 3)

    def test_suppressCaseByTraceLength(self):
        s = Supression(self.getTestXesPath())

        no_traces = len(s.xesLog)
        no_events = sum([len(trace) for trace in s.xesLog])
        self.assertEqual(no_traces, 6)
        self.assertEqual(no_events, 42)

        s.SuppressCaseByTraceLength(5)

        no_traces = len(s.xesLog)
        no_events = sum([len(trace) for trace in s.xesLog])
        self.assertEqual(no_traces, 4)
        self.assertEqual(no_events, 20)
