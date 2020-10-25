from ppdp_anonops.anonymizationOperationInterface import anonymizationOperationInterface
from pm4py.objects.log.importer.xes import factory as xes_importer_factory
import hashlib


class supression(anonymizationOperationInterface):
    """Replace a """

    def __init__(self, xesLogPath):
        super(supression, self).__init__(xesLogPath)

    def Process(self, xes_path: str, parameter) -> str:
        xes_log = xes_importer_factory.apply(xes_path)
        no_traces = len(xes_log)
        no_events = sum([len(trace) for trace in xes_log])
        result = None

        if (parameter['OP_Level'] == 'event' and parameter['OP_Target'] == 'event'):
            # Event based supression: If an event has a certain activity value it is removed from the trace
            for case_index, case in enumerate(xes_log):
                for event_index, event in enumerate(case):
                    result = {'Event': event}
                    # for key in event.keys():
                    #    if key not in event_attribs:
                    #        event_attribs.append(key)

        elif (parameter['OP_Level'] == 'Case' and parameter['OP_Target'] == 'Case'):
            result = self.suppressCaseByTraceLength(8)
        elif (parameter['OP_Level'] == 'event' and parameter['OP_Target'] == 'resource'):
            result = None
        else:
            raise NotImplementedError
        return {'Operation': 'Supression', 'Result': result}
        pass

    def suppressEvent(self, supressedActivity, supressedActivityValue):
        for t_idx, trace in enumerate(self.xesLog):
            # filter out all the events with matching activity values - supressedActivity "concept:name" at event level typically represents the performed activity
            trace[:] = [event for event in trace if event[supressedActivity] != supressedActivityValue]
        self.AddExtension('Supression', 'Event', 'Event')

    def suppressCaseByTraceLength(self, maxLength):
        # Filter for cases with acceptable length
        self.xesLog[:] = [trace for trace in self.xesLog if len(trace) <= maxLength]
        self.AddExtension('Supression', 'Case', 'Case')

    def suppressEventAttribute(self, matchAttribute, matchAttributeValue, supressedAttribute):
        for case_index, case in enumerate(self.xesLog):
            for event_index, event in enumerate(case):
                if (event[matchAttribute] == matchAttributeValue):
                    # Only supress resource if activity value is a match
                    event[supressedAttribute] = None
        self.AddExtension('Supression', 'Event', supressedAttribute)
