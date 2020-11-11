from .anonymizationOperationInterface import AnonymizationOperationInterface
from .utils import TaxonomyTree


class Generalization(AnonymizationOperationInterface):

    def __init__(self):
        super(Generalization, self).__init__()

    def GeneralizeEventAttributeByTaxonomyTreeDepth(self, xesLog, sensitiveAttribute, taxonomyTree, depth):
        taxDict = taxonomyTree.GetGeneralizedDict_NodeNameToDepthXParentalName(depth)

        # Replace all attribute values below 'depth' in the taxTree with their generalized parental value
        for case_index, case in enumerate(xesLog):
            for event_index, event in enumerate(case):
                if sensitiveAttribute in event.keys():
                    if event[sensitiveAttribute] in taxDict.keys():
                        event[sensitiveAttribute] = taxDict[event[sensitiveAttribute]]
        self.AddExtension(xesLog, 'Generalization', 'Event', sensitiveAttribute)

        return xesLog

    def GeneralizeCaseAttributeByTaxonomyTreeDepth(self, xesLog, sensitiveAttribute, taxonomyTree, depth):
        taxDict = taxonomyTree.GetGeneralizedDict_NodeNameToDepthXParentalName(depth)

        # Replace all attribute values below 'depth' in the taxTree with their generalized parental value
        for case_index, case in enumerate(xesLog):
            if sensitiveAttribute in case.keys():
                if case[sensitiveAttribute] in taxDict.keys():
                    case[sensitiveAttribute] = taxDict[case[sensitiveAttribute]]
        self.AddExtension(xesLog, 'Generalization', 'Case', sensitiveAttribute)
        return xesLog

    def GeneralizeEventTimeAttribute(self, xesLog, dateTimeAttribute, generalizationLevel):
        for case_index, case in enumerate(xesLog):
            for event_index, event in enumerate(case):
                if(generalizationLevel == "seconds"):
                    event[dateTimeAttribute] = event[dateTimeAttribute].replace(microsecond=0)

                if(generalizationLevel == "minutes"):
                    event[dateTimeAttribute] = event[dateTimeAttribute].replace(microsecond=0, second=0)

                if(generalizationLevel == "hours"):
                    event[dateTimeAttribute] = event[dateTimeAttribute].replace(microsecond=0, second=0, minute=0)

                if(generalizationLevel == "days"):
                    event[dateTimeAttribute] = event[dateTimeAttribute].replace(microsecond=0, second=0, minute=0, hour=0)

                if(generalizationLevel == "months"):
                    event[dateTimeAttribute] = event[dateTimeAttribute].replace(microsecond=0, second=0, minute=0, hour=0, day=1)

                if(generalizationLevel == "years"):
                    event[dateTimeAttribute] = event[dateTimeAttribute].replace(microsecond=0, second=0, minute=0, hour=0, day=1, month=1)

        self.AddExtension(xesLog, 'Generalization', 'Event', dateTimeAttribute)
        return xesLog
