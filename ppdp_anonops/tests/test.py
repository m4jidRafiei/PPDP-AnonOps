
from pm4py.objects.log.importer.xes import factory as xes_importer
from pm4py.objects.log.exporter.xes import factory as xes_exporter
import hashlib
from cryptography.fernet import Fernet
from ppdp_anonops import Condensation, Swapping, Addition
import base64
from math import sqrt
from ppdp_anonops.utils import *
from sklearn.cluster import KMeans

# running_example.xes
# Traces: 6
# Events 42
import numpy as np
from kmodes.kmodes import KModes

from sklearn.preprocessing import OneHotEncoder


def main():
    log = xes_importer.apply("resources/Sepsis Cases - Event Log.xes")

    vals = []
    for case_index, case in enumerate(log):
        for eIdx, e in enumerate(case):
            if(e["concept:name"] not in vals):
                vals.append(e["concept:name"])

    enc = OneHotEncoder(handle_unknown='ignore')
    vals = np.array(vals).reshape(-1, 1)
    enc.fit(vals)

    encDict = {}
    decDict = {}
    data = enc.transform(vals).toarray()
    cat = enc.categories_[0]
    for i in range(len(cat)):
        encDict[cat[i]] = data[i]
        #decDict[data[i]] = cat[i]

    print(encDict)
    print('###############')
    print(decDict)

    # initialize KMeans object specifying the number of desired clusters
    kmeans = KMeans(n_clusters=5)

    # reshape data to make them clusterable
    readyData = data  # np.array(data).reshape(-1, 1)

    # learning the clustering from the input date
    kmeans.fit(readyData)

    print(kmeans.labels_)


def euclidianDistance(weights, attributesA, attributesB):
    if(len(weights) != len(attributesA) != len(attributesB)):
        raise NotImplementedError("This feature is only available for input arrays of identical length")

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
