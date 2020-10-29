from ppdp_anonops.anonymizationOperationInterface import anonymizationOperationInterface


class generalization(anonymizationOperationInterface):

    def __init__(self, xesLogPath):
        super(generalization, self).__init__(xesLogPath)

    def generalizeEventTimeAttribute(self, dateTimeAttribute, generalizationLevel):
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
