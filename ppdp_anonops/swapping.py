from .anonymizationOperationInterface import AnonymizationOperationInterface
import collections
import random

# k-means
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
import numpy as np
import numbers

from ppdp_anonops.utils import euclidClusterHelper


class Swapping(AnonymizationOperationInterface):
    def __init__(self):
        super(Swapping, self).__init__()

    def SwapEventAttributeValuesBykMeanCluster(self, xesLog, sensitiveAttribute, descriptiveAttributes, k_clusters):
        allAttributes = descriptiveAttributes.copy()
        allAttributes.append(sensitiveAttribute)

        values = self._getEventMultipleAttributeValues(xesLog, allAttributes)
        values, valueToOneHotDict, oneHotToValueDict = euclidClusterHelper.oneHotEncodeNonNumericAttributes(allAttributes, values)

        kmeans = KMeans(n_clusters=k_clusters)
        kmeans.fit(values)

        # Get a dict with the value as key and the cluster it is assigned to as value
        valueToClusterDict = self.__getValuesOfSensitiveAttributePerClusterAsDict(kmeans.labels_, values)

        # If OneHot encoding was used: Ensure the mapping dicts are working with the original values, not the OneHot values
        if(sensitiveAttribute in valueToOneHotDict.keys()):
            clusterToValuesDict = {k: [oneHotToValueDict[sensitiveAttribute][x] for x in valueToClusterDict.keys() if valueToClusterDict[x] == k] for k in range(k_clusters)}
            valueToClusterDict = {oneHotToValueDict[sensitiveAttribute][x]: valueToClusterDict[x] for x in valueToClusterDict.keys()}
        else:
            clusterToValuesDict = {k: [x for x in valueToClusterDict.keys() if valueToClusterDict[x] == k] for k in range(k_clusters)}

        # Choose random new value from clustered data
        for case_index, case in enumerate(xesLog):
            for event_index, event in enumerate(case):
                if(sensitiveAttribute in event.keys()):
                    # Get possible values from current values cluster
                    listOfValues = clusterToValuesDict[valueToClusterDict[event[sensitiveAttribute]]]

                    # Generate new random index
                    rnd = random.randint(0, len(listOfValues) - 1)

                    # Overwrite old attribute value with new one
                    event[sensitiveAttribute] = listOfValues[rnd]

        self.AddExtension(xesLog, 'swa', 'event', sensitiveAttribute)
        return xesLog

    def SwapCaseAttributeValuesBykMeanCluster(self, xesLog, sensitiveAttribute, descriptiveAttributes, k_clusters):
        allAttributes = descriptiveAttributes.copy()
        allAttributes.append(sensitiveAttribute)

        values = self._getCaseMultipleAttributeValues(xesLog, allAttributes)
        values, valueToOneHotDict, oneHotToValueDict = euclidClusterHelper.oneHotEncodeNonNumericAttributes(allAttributes, values)

        kmeans = KMeans(n_clusters=k_clusters)
        kmeans.fit(values)

        # Get a dict with the value as key and the cluster it is assigned to as value
        valueToClusterDict = self.__getValuesOfSensitiveAttributePerClusterAsDict(kmeans.labels_, values)

        # If OneHot encoding was used: Ensure the mapping dicts are working with the original values, not the OneHot values
        if(sensitiveAttribute in valueToOneHotDict.keys()):
            clusterToValuesDict = {k: [oneHotToValueDict[sensitiveAttribute][x] for x in valueToClusterDict.keys() if valueToClusterDict[x] == k] for k in range(k_clusters)}
            valueToClusterDict = {oneHotToValueDict[sensitiveAttribute][x]: valueToClusterDict[x] for x in valueToClusterDict.keys()}
        else:
            clusterToValuesDict = {k: [x for x in valueToClusterDict.keys() if valueToClusterDict[x] == k] for k in range(k_clusters)}

        # Choose random new value from clustered data
        for case_index, case in enumerate(xesLog):
            if(sensitiveAttribute in case.attributes.keys()):
                # Get possible values from current values cluster
                listOfValues = clusterToValuesDict[valueToClusterDict[case.attributes[sensitiveAttribute]]]

                # Generate new random index
                rnd = random.randint(0, len(listOfValues) - 1)

                # Overwrite old attribute value with new one
                case.attributes[sensitiveAttribute] = listOfValues[rnd]

        self.AddExtension(xesLog, 'swa', 'case', sensitiveAttribute)
        return xesLog

    # Make sure all values provided are actually numeric
    def __checkNumericAttributes(self, values):
        numCheck = [x for x in values if not isinstance(x, numbers.Number)]
        if(len(numCheck) > 0):
            raise NotImplementedError("Use a numeric attribute")
        pass

    def __getValuesOfSensitiveAttributePerClusterAsDict(self, clusterLabels, values):
        valueToClusterDict = {}
        for i in range(len(clusterLabels)):
            # [-1] as the sensitive attribute value is always the last in the list
            if values[i][-1] not in valueToClusterDict.keys():
                valueToClusterDict[values[i][-1]] = clusterLabels[i]
        return valueToClusterDict
