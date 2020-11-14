from .anonymizationOperationInterface import AnonymizationOperationInterface
import random


class Substitution(AnonymizationOperationInterface):

    def __init__(self):
        super(Substitution, self).__init__()

    def SubstituteEventAttributeValue(self, xesLog, matchAttribute, sensitiveAttributeValues):
        insensitiveAttributes = []
        for case_index, case in enumerate(xesLog):
            for event_index, event in enumerate(case):
                if (matchAttribute in event.keys() and event[matchAttribute] not in insensitiveAttributes and event[matchAttribute] not in sensitiveAttributeValues):
                    insensitiveAttributes.append(event[matchAttribute])

        for case_index, case in enumerate(xesLog):
            for event_index, event in enumerate(case):
                if (matchAttribute in event.keys() and event[matchAttribute] in sensitiveAttributeValues):
                    event[matchAttribute] = insensitiveAttributes[random.randint(0, len(insensitiveAttributes) - 1)]

        return self.AddExtension(xesLog, 'sub', 'Event', matchAttribute)
