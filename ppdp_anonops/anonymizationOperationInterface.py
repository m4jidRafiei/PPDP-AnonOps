import abc
from pm4py.objects.log.importer.xes import factory as xes_importer
from pm4py.objects.log.exporter.xes import factory as xes_exporter

from p_privacy_metadata.privacyExtension import privacyExtension


class anonymizationOperationInterface(metaclass=abc.ABCMeta):
    def __init__(self, xesLogPath):
        self.xesLogPath = xesLogPath
        self.xesLog = xes_importer.apply(xesLogPath)

    # @classmethod
    # def __subclasshook__(cls, subclass):
    #     return (hasattr(subclass, 'Process') and callable(subclass.Process))

    # @abc.abstractmethod
    # def Process(self, path: str, parameter):
    #     """Perform the anonymization operation on th xes log"""
    #     raise NotImplementedError

    def ExportLog(self, xesExportLogPath):
        xes_exporter.export_log(self.xesLog, xesExportLogPath)

    def AddExtension(self, anonOp, level, target):
        # adding privacy extension here....
        prefix = 'privacy:'
        uri = 'paper_version_uri/privacy.xesext'

        privacy = privacyExtension(self.xesLog, prefix, uri)

        #privacy.set_anonymizer('substitution', 'event', 'concept:name')
        privacy.set_anonymizer(anonOp, level, target)
        # End of adding extension
