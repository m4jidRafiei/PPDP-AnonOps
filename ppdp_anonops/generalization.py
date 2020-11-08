from .anonymizationOperationInterface import AnonymizationOperationInterface
from .utils import TaxonomyTree


class Generalization(AnonymizationOperationInterface):

    def __init__(self, xesLogPath):
        super(Generalization, self).__init__(xesLogPath)

# generalization by taxonomy tree

    def GeneralizeEventAttributeByTaxonomyTreeDepth(self, sensitiveAttribute, taxonomyTree, depth):
        taxDict = taxonomyTree.GetGeneralizedDict_NodeNameToDepthXParentalName(depth)

        # Replace all attribute values below 'depth' in the taxTree with their generalized parental value
        for case_index, case in enumerate(self.xesLog):
            for event_index, event in enumerate(case):
                if sensitiveAttribute in event.keys():
                    if event[sensitiveAttribute] in taxDict.keys():
                        event[sensitiveAttribute] = taxDict[event[sensitiveAttribute]]

    def GeneralizeCaseAttributeByTaxonomyTreeDepth(self, sensitiveAttribute, taxonomyTree, depth):
        taxDict = taxonomyTree.GetGeneralizedDict_NodeNameToDepthXParentalName(depth)

        # Replace all attribute values below 'depth' in the taxTree with their generalized parental value
        for case_index, case in enumerate(self.xesLog):
            if sensitiveAttribute in case.keys():
                if case[sensitiveAttribute] in taxDict.keys():
                    case[sensitiveAttribute] = taxDict[case[sensitiveAttribute]]

    def GeneralizeEventTimeAttribute(self, dateTimeAttribute, generalizationLevel):
        for case_index, case in enumerate(self.xesLog):
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

                #self.AddExtension('generalization', 'Event', dateTimeAttribute)
