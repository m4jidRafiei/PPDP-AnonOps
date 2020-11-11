from .anonymizationOperationInterface import AnonymizationOperationInterface
from pm4py.objects.log.importer.xes import factory as xes_importer_factory
import hashlib


class Supression(AnonymizationOperationInterface):
    """Replace a """

    def __init__(self):
        super(Supression, self).__init__()

    def SuppressEvent(self, xesLog, supressedActivity, supressedActivityValue):
        for t_idx, trace in enumerate(xesLog):
            # filter out all the events with matching activity values - supressedActivity "concept:name" at event level typically represents the performed activity
            trace[:] = [event for event in trace if event[supressedActivity] != supressedActivityValue]
        self.AddExtension(xesLog, 'Supression', 'Event', 'Event')
        return xesLog

    def SuppressCaseByTraceLength(self, xesLog, maxLength):
        # Filter for cases with acceptable length
        xesLog[:] = [trace for trace in xesLog if len(trace) <= maxLength]
        self.AddExtension(xesLog, 'Supression', 'Case', 'Case')
        return xesLog

    def SuppressEventAttribute(self, xesLog, matchAttribute, matchAttributeValue, supressedAttribute):
        for case_index, case in enumerate(xesLog):
            for event_index, event in enumerate(case):
                if (event[matchAttribute] == matchAttributeValue):
                    # Only supress resource if activity value is a match
                    event[supressedAttribute] = None
        self.AddExtension(xesLog, 'Supression', 'Event', supressedAttribute)
        return xesLog
