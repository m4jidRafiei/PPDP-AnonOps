from ppdp_anonops.anonymizationOperationInterface import anonymizationOperationInterface
import collections

# k-means
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
import numpy as np
import numbers


class condensation(anonymizationOperationInterface):

    def __init__(self, xesLogPath):
        super(condensation, self).__init__(xesLogPath)

    # Possibly realize by k-means clustering
    # def condenseNumericalAttribute(self, sensitiveAttribute):

    def condenseEventAttributeBykMeanClusterMode(self, sensitiveAttribute, k_clusters):
        values = self._getEventAttributeValues(sensitiveAttribute)

        self.__checkNumericAttributes(values)

        kmeans = self.__clusterizeData(values, k_clusters)

        valueClusterDict, clusterMode = self.__getClusterHelpers(kmeans, values)

        # Apply clustered data mode to log
        for case_index, case in enumerate(self.xesLog):
            for event_index, event in enumerate(case):
                if(sensitiveAttribute in event.keys()):
                    event[sensitiveAttribute] = clusterMode[valueClusterDict[event[sensitiveAttribute]]]
        print(clusterMode)
        self.AddExtension('con', 'event', sensitiveAttribute)

    def condenseCaseAttributeUsingMode(self, sensitiveAttribute, k_clusters):
        values = self._getCaseAttributeValues(sensitiveAttribute)

        self.__checkNumericAttributes(values)

        kmeans = self.__clusterizeData(values, k_clusters)

        valueClusterDict, clusterMode = self.__getClusterHelpers(kmeans, values)

        # Apply clustered data mode to log
        for case_index, case in enumerate(self.xesLog):
            if(sensitiveAttribute in case.keys()):
                case[sensitiveAttribute] = clusterMode[valueClusterDict[case[sensitiveAttribute]]]

        self.AddExtension('con', 'case', sensitiveAttribute)

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

    # Make sure all values provided are actually numeric
    def __checkNumericAttributes(self, values):
        numCheck = [x for x in values if not isinstance(x, numbers.Number)]
        if(len(numCheck) > 0):
            raise NotImplementedError("Use a numeric attribute")
        pass

    def __clusterizeData(self, values, k_clusters):
        # initialize KMeans object specifying the number of desired clusters
        kmeans = KMeans(n_clusters=k_clusters)

        # reshape data to make them clusterable
        readyData = np.array(values).reshape(-1, 1)

        # learning the clustering from the input date
        kmeans.fit(readyData)

        return kmeans

    def __getClusterHelpers(self, kmeans, values):
        # Provides a cluster number for every key
        valueClusterDict = {}
        for i in range(len(kmeans.labels_)):
            if values[i] not in valueClusterDict:
                valueClusterDict[values[i]] = kmeans.labels_[i]

        clusterMode = {}
        for i in range(kmeans.n_clusters):
            clusterMode[i] = self.__getMode([x for x in valueClusterDict.keys() if valueClusterDict[x] == i])

        return valueClusterDict, clusterMode
