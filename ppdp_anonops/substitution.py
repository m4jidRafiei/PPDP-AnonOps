from ppdp_anonops.anonymizationOperationInterface import anonymizationOperationInterface
import random


class substitution(anonymizationOperationInterface):

    def __init__(self, xesLogPath):
        super(substitution, self).__init__(xesLogPath)

    def substituteEventAttributeValue(self, matchAttribute, sensitiveAttributeValues):
        insensitiveAttributes = []
        for case_index, case in enumerate(self.xesLog):
            for event_index, event in enumerate(case):
                if event[matchAttribute] not in insensitiveAttributes and event[matchAttribute] not in sensitiveAttributeValues:
                    insensitiveAttributes.append(event[matchAttribute])

        print(*insensitiveAttributes, sep=", ")
        print(*sensitiveAttributeValues, sep=", ")

        for case_index, case in enumerate(self.xesLog):
            for event_index, event in enumerate(case):
                if (event[matchAttribute] in sensitiveAttributeValues):
                    event[matchAttribute] = insensitiveAttributes[random.randint(0, len(insensitiveAttributes) - 1)]
                    print("Treffer")

        self.AddExtension('sub', 'Event', matchAttribute)