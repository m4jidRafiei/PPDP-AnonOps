from unittest import TestCase
import os
from ppdp_anonops.substitution import substitution


class TestSubstitution(TestCase):
    def getTestXesPath(self):
        return os.path.join(os.path.dirname(__file__), 'resources', 'running_example.xes')

    def test_substituteResources(self):
        s = substitution(self.getTestXesPath())

        frequency = {"Sean": 0, "Sara": 0}
        for case_index, case in enumerate(s.xesLog):
            for event_index, event in enumerate(case):
                if event["org:resource"] in frequency.keys():
                    frequency[event["org:resource"]] += 1

        self.assertGreater(frequency["Sean"], 0)
        self.assertGreater(frequency["Sara"], 0)

        s.substituteEventAttributeValue("org:resource", ["Sean", "Sara"])

        frequency = {"Sean": 0, "Sara": 0}
        for case_index, case in enumerate(s.xesLog):
            for event_index, event in enumerate(case):
                if event["org:resource"] in frequency.keys():
                    frequency[event["org:resource"]] += 1

        self.assertEqual(frequency["Sean"], 0)
        self.assertEqual(frequency["Sara"], 0)
