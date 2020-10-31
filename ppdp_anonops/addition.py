from ppdp_anonops.anonymizationOperationInterface import anonymizationOperationInterface
from copy import deepcopy
import random
from datetime import timedelta


class addition(anonymizationOperationInterface):
    """Extract text from a PDF."""

    def __init__(self, xesLogPath):
        super(addition, self).__init__(xesLogPath)

    def addEvent(self, matchAttribute, matchAttributeValue):
        for case_index, case in enumerate(self.xesLog):
            traceLength = len(case)
            firstCase = case[0]
            lastCase = case[traceLength - 1]

            if(lastCase[matchAttribute] == matchAttributeValue):
                newEvent = deepcopy(case[traceLength - 1])

                # Randomly generate timestamp after the last trace
                secDelta = random.randint(0, (lastCase["time:timestamp"] - firstCase["time:timestamp"]).total_seconds())
                newEvent["time:timestamp"] = newEvent["time:timestamp"] + timedelta(seconds=secDelta)

                case.append(newEvent)
        self.AddExtension("add", "case", "trace")

    # def addEventAtRandomPlaceInTrace(self):
    # def addEventFirstInTrace(self):
    # def addEventLastInTrace(self):
