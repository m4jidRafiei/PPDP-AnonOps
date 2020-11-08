
from pm4py.objects.log.importer.xes import factory as xes_importer_factory
from pm4py.objects.log.exporter.xes import factory as xes_exporter
import hashlib
from cryptography.fernet import Fernet
from ppdp_anonops import Condensation, Swapping
import base64
from math import sqrt

# running_example.xes
#Traces: 6
# Events 42
import numpy as np
from kmodes.kmodes import KModes


def main():
    xes_log = xes_importer_factory.apply("resources/Sepsis Cases - Event Log.xes")

    # random categorical data
    data = np.random.choice(20, (100, 10))

    km = KModes(n_clusters=4, init='Huang', n_init=5, verbose=1)

    clusters = km.fit_predict(xes_log)

    # Print the cluster centroids
    print(km.cluster_centroids_)

    #s = condensation("resources/Sepsis Cases - Event Log.xes")
    #s.condenseEventAttributeBykMeanClusterMode("CRP", 5)
    # s.ExportLog("resources/tmp2.xes")

    s = Swapping("resources/Sepsis Cases - Event Log.xes")
    s.SwapEventAttributeValuesBykMeanCluster("CRP", 5)
    s.ExportLog("resources/tmp2.xes")

    print("no_traces = " + str(len(s.xesLog)))
    print("no_events = " + str(sum([len(trace) for trace in s.xesLog])))


def euclidianDistance(weights, attributesA, attributesB):
    if(len(weights) != len(attributesA) != len(attributesB)):
        raise

    sum = 0

    for i in range(len(weights)):
        sum += weights[i] * ((attributesA[i] - attributesB[i]) ** 2)

    return sqrt(sum)


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

# Identity (Case) Disclosure
# def calculateIdentityCaseDisclosure():


# Attribute (Trace) Disclosure
# def calculateAttributeTraceDisclosure():


# def calculateUtilityLoss():


if __name__ == "__main__":
    main()
