from .anonymizationOperationInterface import AnonymizationOperationInterface
from copy import deepcopy
import random
from datetime import timedelta


class Addition(AnonymizationOperationInterface):
    """Extract text from a PDF."""

    def __init__(self):
        super(Addition, self).__init__()

    # give user opportunity to design the newly added event! (06.11.20 / Meeting with Majid)

    def AddEvent(self, xesLog, matchAttribute, matchAttributeValue):
        # event based not case based
        for case_index, case in enumerate(xesLog):
            traceLength = len(case)
            firstCase = case[0]
            lastCase = case[traceLength - 1]

            if(lastCase[matchAttribute] == matchAttributeValue):
                newEvent = deepcopy(case[traceLength - 1])

                # Randomly generate timestamp after the last trace
                secDelta = random.randint(0, (lastCase["time:timestamp"] - firstCase["time:timestamp"]).total_seconds())
                newEvent["time:timestamp"] = newEvent["time:timestamp"] + timedelta(seconds=secDelta)

                case.append(newEvent)
        self.AddExtension(xesLog, "add", "case", "trace")
        return xesLog
    # def addEventAtRandomPlaceInTrace(self):
    # def addEventFirstInTrace(self):
    # def addEventLastInTrace(self):
