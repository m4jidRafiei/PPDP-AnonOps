from .anonymizationOperationInterface import AnonymizationOperationInterface
from pm4py.objects.log.importer.xes import factory as xes_importer_factory
import hashlib


class Supression(AnonymizationOperationInterface):
    """Replace a """

    def __init__(self):
        super(Supression, self).__init__()

    def SuppressEvent(self, xesLog, matchAttribute, matchAttributeValue):
        for t_idx, trace in enumerate(xesLog):
            # filter out all the events with matching attribute values - matchAttribute "concept:name" at event level typically represents the performed activity
            trace[:] = [event for event in trace if (matchAttribute not in event.keys() or event[matchAttribute] != matchAttributeValue)]
        return self.AddExtension(xesLog, 'Supression', 'Event', 'Event')

    def SuppressCaseByTraceLength(self, xesLog, maxLength):
        # Filter for cases with acceptable length
        xesLog[:] = [trace for trace in xesLog if len(trace) <= maxLength]
        return self.AddExtension(xesLog, 'Supression', 'Case', 'Case')

    def SuppressEventAttribute(self, xesLog, supressedAttribute, matchAttribute=None, matchAttributeValue=None):
        for case_index, case in enumerate(xesLog):
            for event_index, event in enumerate(case):
                isMatch = (matchAttribute is None and matchAttributeValue is None) or (matchAttribute in event.keys() and event[matchAttribute] == matchAttributeValue)

                if (isMatch):
                    # Only supress resource if activity value is a match
                    event[supressedAttribute] = None
        return self.AddExtension(xesLog, 'Supression', 'Event', supressedAttribute)
