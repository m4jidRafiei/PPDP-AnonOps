
from pm4py.objects.log.importer.xes import factory as xes_importer_factory
from pm4py.objects.log.exporter.xes import factory as xes_exporter
import hashlib
from cryptography.fernet import Fernet
from ppdp_anonops.condensation import condensation
from ppdp_anonops.swapping import swapping
import base64
# running_example.xes
#Traces: 6
# Events 42


def main():
    #xes_log = xes_importer_factory.apply("resources/running_example.xes")
    #print("no_traces = " + str(len(xes_log)))
    #print("no_events = " + str(sum([len(trace) for trace in xes_log])))

    #s = condensation("resources/running_example.xes")

    #s = condensation("resources/Sepsis Cases - Event Log.xes")
    #s.condenseEventAttributeBykMeanClusterMode("CRP", 5)
    # s.ExportLog("resources/tmp2.xes")

    s = swapping("resources/Sepsis Cases - Event Log.xes")
    s.swapEventAttributeValuesBykMeanCluster("CRP", 5)
    s.ExportLog("resources/tmp2.xes")

    print("no_traces = " + str(len(s.xesLog)))
    print("no_events = " + str(sum([len(trace) for trace in s.xesLog])))


def getAttr(xes_log):
    case_attribs = []
    for case_index, case in enumerate(xes_log):
        for key in case.attributes.keys():
            if key not in case_attribs:
                case_attribs.append(key)
    event_attribs = []
    for case_index, case in enumerate(xes_log):
        for event_index, event in enumerate(case):
            for key in event.keys():
                if key not in event_attribs:
                    event_attribs.append(key)
    return case_attribs, event_attribs


if __name__ == "__main__":
    main()
