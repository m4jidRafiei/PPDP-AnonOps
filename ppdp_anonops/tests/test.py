
from pm4py.objects.log.importer.xes import factory as xes_importer
from pm4py.objects.log.exporter.xes import factory as xes_exporter
import hashlib
from cryptography.fernet import Fernet
from ppdp_anonops import Condensation, Swapping, Addition
import base64
from math import sqrt
from ppdp_anonops.utils import *
from sklearn.cluster import KMeans
import random
import numpy as np
from kmodes.kmodes import KModes
import numbers

from sklearn.preprocessing import OneHotEncoder

from ppdp_anonops.utils import euclidClusterHelper


def main():
    log = xes_importer.apply("resources/running_exampleWithCaseAttributes.xes")
    #c = Condensation()
    #log = c.CondenseCaseAttributeBykMeanClusterUsingMode(log, "Age", ["concept:name", "Zip"], 3)
    #log = c.CondenseEventAttributeBykModeCluster(log, "Leader", ["concept:name", "Zip"], 3)
    s = Swapping()
    s.SwapCaseAttributeValuesBykMeanCluster(log, "Leader", ["concept:name", "Zip"], 4)
    #s.SwapCaseAttributeValuesBykMeanCluster(log, "Age", ["concept:name", "Zip"], 3)
    xes_exporter.export_log(log, "tmpEuclid.xes")

    # sensitiveAttribute = "Age"
    # descriptiveAttributes = ["concept:name", "Zip", "Leader"]
    # allAttributes = ["Age"]  # ["concept:name", "Zip", "Leader", "Age"]
    # k_clusters = 5

    # values = _getCaseAttributeValues(log, allAttributes)
    # print(values, sep=',')
    # values = euclidClusterHelper.oneHotEncodeNonNumericAttributes(values)
    # print(values, sep=',')

    # # initialize KMeans object specifying the number of desired clusters
    # kmeans = KMeans(n_clusters=k_clusters)
    # # reshape data to make them clusterable
    # readyData = values  # np.array(values).reshape(-1, 1)
    # # learning the clustering from the input date
    # kmeans.fit(readyData)

    # print(kmeans.labels_)
    # print(kmeans.cluster_centers_)

    # valueClusterDict = __getValueToCluster(kmeans, values)
    # clusterMode = __getClusterMode(kmeans, values)

    # # Apply clustered data mode to log
    # for case_index, case in enumerate(log):
    #     for event_index, event in enumerate(case):
    #         if(sensitiveAttribute in event.keys()):
    #             event[sensitiveAttribute] = clusterMode[valueClusterDict[event[sensitiveAttribute]]]

    ## log = c.CondenseEventAttributeBykModeCluster(log, "concept:name", ["org:group", "CRP", "LacticAcid"], 5)
    ## xes_exporter.export_log(log, "tmp.xes")


def kModes():
    log = xes_importer.apply("resources/Sepsis Cases - Event Log.xes")
    vals = []
    for case_index, case in enumerate(log):
        for eIdx, e in enumerate(case):
            if((e["concept:name"], e["org:group"]) not in vals):
                vals.append((e["concept:name"], e["org:group"]))

    km = KModes(n_clusters=4, init='Huang', n_init=5, verbose=1)

    # clusters = km.fit_predict(np.array(vals).reshape(-1, 1))
    clusters = km.fit_predict(vals)

    # Print the cluster centroids
    print(km.cluster_centroids_)
    print(km.labels_)

    for i in range(len(vals)):
        print(str(km.cluster_centroids_[km.labels_[i]]) + " => " + str(vals[i]))


def euclidDistClusterCase(log, sensitiveAttribute, descriptiveAttributes, k, verboose=0):
    # Move Unique-Event-Attributes up to trace attributes
    attributes = descriptiveAttributes
    attributes.append(sensitiveAttribute)
    log = liftUniqueEventAttributesToCase(log, attributes)

    # Randomly select k cases to be the centroids of our clustering
    clusterCentroids = []
    try:
        for i in random.sample(range(0, len(log)), k):
            clusterCentroids.append(log[i])
    except ValueError:
        raise ValueError("Choose a suitable amount of clusters: k < " + str(len(log)))

    # When a selected attribute is not of a numeric type => One-Hot encode it
    oneHotEncodedDict = {}
    for attr in attributes:
        for case_index, case in enumerate(log):
            if not isinstance(case.attributes[attr], numbers.Number) and attr not in oneHotEncodedDict:
                oneHotEncodedDict[attr] = {'Values': [], 'OneHotEncoded': [], 'OneHotSkalar': [], 'ValueToIndex': {}}
    for attr in oneHotEncodedDict.keys():
        for case_index, case in enumerate(log):
            if case.attributes[attr] not in oneHotEncodedDict[attr]['Values']:
                oneHotEncodedDict[attr]['Values'].append(case.attributes[attr])
                oneHotEncodedDict[attr]['ValueToIndex'][case.attributes[attr]] = len(oneHotEncodedDict[attr]['Values']) - 1
        for i in range(0, len(oneHotEncodedDict[attr]['Values'])):
            # Create OneHot-Tuple
            t = [0, ]*len(oneHotEncodedDict[attr]['Values'])
            t[i] = 1
            oneHotEncodedDict[attr]['OneHotEncoded'].append(tuple(t))
            #oneHotEncodedDict[attr]['OneHotSkalar'].append(2 * i)
            #oneHotEncodedDict[attr]['OneHotSkalar'].append((2 + i) * i)
            oneHotEncodedDict[attr]['OneHotSkalar'].append(1 + ((i * 1.0) / len(oneHotEncodedDict[attr]['Values'])))

    if(verboose == 1):
        print("######################### OneHot-Encoding #########################")
        print(oneHotEncodedDict.keys())
        print("###################################################################")

    caseClusters = []
    for case_index, case in enumerate(log):
        val = [(oneHotEncodedDict[i]['OneHotSkalar'][oneHotEncodedDict[i]['ValueToIndex'][case.attributes[i]]] if i in oneHotEncodedDict.keys() else case.attributes[i]) for i in attributes]

        centroidDistance = []
        for centroid in clusterCentroids:
            centroidVals = [(oneHotEncodedDict[i]['OneHotSkalar'][oneHotEncodedDict[i]['ValueToIndex'][centroid.attributes[i]]] if i in oneHotEncodedDict.keys() else centroid.attributes[i]) for i in attributes]
            centroidDistance.append(euclidianDistance([0.1, 0.1, 0.8], val, centroidVals))
        caseClusters.append(np.argmin(centroidDistance))

    if(verboose == 1):
        print("######################### Cluster of Case (Array-Index is Case-Index) #########################")
        print(caseClusters)
        print("###############################################################################################")


def euclidianDistance(weights, attributesA, attributesB):
    if(len(weights) != len(attributesA) != len(attributesB)):
        raise NotImplementedError("This feature is only available for input arrays of identical length")

    sum = 0

    for i in range(len(weights)):
        sum += weights[i] * ((attributesA[i] - attributesB[i]) ** 2)

        print(str(weights[i]) + " * " + "((" + str(attributesA[i]) + " - " + str(attributesB[i]) + ") ** 2)) = " + str(weights[i] * ((attributesA[i] - attributesB[i]) ** 2)))
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

def __getMode(self, valueList):
    if len(valueList) == 0:
        return 0

    s = {}
    for v in valueList:
        if v in s:
            s[v] += 1
        else:
            s[v] = 1

    # Sort dict by value
    s = {k: v for k, v in sorted(s.items(), key=lambda item: item[1])}
    return next(iter(s.keys()))


def __getValueToCluster(kmeans, values):
    # Provides a cluster number for every key
    valueClusterDict = {}
    for i in range(len(kmeans.labels_)):
        if values[i] not in valueClusterDict:
            valueClusterDict[values[i]] = kmeans.labels_[i]
    return valueClusterDict


def __getClusterMode(kmeans, values):
    valueClusterDict = __getValueToCluster(kmeans, values)

    clusterMode = {}
    for i in range(kmeans.n_clusters):
        clusterMode[i] = __getMode([x for x in valueClusterDict.keys() if valueClusterDict[x] == i])

    return clusterMode


def _getCaseAttributeValues(xesLog, attributes):
    values = []

    for case_index, case in enumerate(xesLog):
        c = []

        for attribute in attributes:
            if(attribute in case.attributes.keys()):
                c.append(case.attributes[attribute])
        values.append(c)

    return values


if __name__ == "__main__":
    main()
