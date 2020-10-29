from unittest import TestCase
import os
from ppdp_anonops.generalization import generalization


class TestGeneralization(TestCase):
    def getTestXesPath(self):
        return os.path.join(os.path.dirname(__file__), 'resources', 'running_example.xes')

    def test_generalizationTime(self):
        s = generalization(self.getTestXesPath())

        no_events = sum([len(trace) for trace in s.xesLog])

        s.generalizeEventTimeAttribute("time:timestamp", "seconds")
        self.assertEquals(self.getTime(s.xesLog, "time:timestamp", "seconds"), 0)

        s.generalizeEventTimeAttribute("time:timestamp", "minutes")
        self.assertEquals(self.getTime(s.xesLog, "time:timestamp", "minutes"), 0)

        s.generalizeEventTimeAttribute("time:timestamp", "hours")
        self.assertEquals(self.getTime(s.xesLog, "time:timestamp", "hours"), 0)

        s.generalizeEventTimeAttribute("time:timestamp", "days")
        self.assertEquals(self.getTime(s.xesLog, "time:timestamp", "days"), 0)

        s.generalizeEventTimeAttribute("time:timestamp", "months")
        self.assertEquals(self.getTime(s.xesLog, "time:timestamp", "months"), no_events)  # no_events as default value for days is 1 and not 0 (0 is an ivalid day-of-month)

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
