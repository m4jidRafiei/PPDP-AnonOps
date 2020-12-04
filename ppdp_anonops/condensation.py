from .anonymizationOperationInterface import AnonymizationOperationInterface
import collections

# k-means
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
import numpy as np
from kmodes.kmodes import KModes
import numbers


class Condensation(AnonymizationOperationInterface):

    def __init__(self):
        super(Condensation, self).__init__()

    # Possibly realize by k-means clustering
    # def condenseNumericalAttribute(self, sensitiveAttribute):

    def CondenseEventAttributeBykMeanClusterUsingMode(self, xesLog, sensitiveAttribute, k_clusters):
        values = self._getEventAttributeValues(xesLog, sensitiveAttribute)

        self.__checkNumericAttributes(values)

        kmeans = self.__clusterizeData(values, k_clusters)

        valueClusterDict = self.__getValueToCluster(kmeans, values)
        clusterMode = self.__getClusterMode(kmeans, values)

        # Apply clustered data mode to log
        for case_index, case in enumerate(xesLog):
            for event_index, event in enumerate(case):
                if(sensitiveAttribute in event.keys()):
                    event[sensitiveAttribute] = clusterMode[valueClusterDict[event[sensitiveAttribute]]]
        print(clusterMode)
        return self.AddExtension(xesLog, 'con', 'event', sensitiveAttribute)

    def CondenseCaseAttributeBykMeanClusterUsingMode(self, xesLog, sensitiveAttribute, k_clusters):
        values = self._getCaseAttributeValues(xesLog, sensitiveAttribute)

        self.__checkNumericAttributes(values)

        kmeans = self.__clusterizeData(values, k_clusters)

        valueClusterDict = self.__getValueToCluster(kmeans, values)
        clusterMode = self.__getClusterMode(kmeans, values)

        # Apply clustered data mode to log
        for case_index, case in enumerate(xesLog):
            if(sensitiveAttribute in case.attributes.keys()):
                case.attributes[sensitiveAttribute] = clusterMode[valueClusterDict[case.attributes[sensitiveAttribute]]]

        return self.AddExtension(xesLog, 'con', 'case', sensitiveAttribute)

    def CondenseEventAttributeBykModeCluster(self, xesLog, sensitiveAttribute, clusterRelevantAttributes, k_clusters):
        # Make sure the sensitive attribute is last in line for later indexing
        if(sensitiveAttribute in clusterRelevantAttributes):
            clusterRelevantAttributes.remove(sensitiveAttribute)
        clusterRelevantAttributes.append(sensitiveAttribute)

        values = self._getEventAttributesTuples(xesLog, clusterRelevantAttributes)

        km = KModes(n_clusters=k_clusters, init='Huang', n_init=5)

        if(len(values[0]) == 1):
            values = np.array(values).reshape(-1, 1)

        clusters = km.fit_predict(values)
        valueClusterDict = self.__getValueToCluster(km, values)

        print(valueClusterDict)
        print(km.cluster_centroids_)

        # Apply clustered data mode to log
        for case_index, case in enumerate(xesLog):
            for event_index, event in enumerate(case):
                if(sensitiveAttribute in event.keys()):
                    t = tuple((event[attribute] if attribute in event.keys() else 0) for attribute in clusterRelevantAttributes)
                    event[sensitiveAttribute] = km.cluster_centroids_[valueClusterDict[t]][-1]

        return self.AddExtension(xesLog, 'con', 'event', sensitiveAttribute)

    def CondenseCaseAttributeBykModeCluster(self, xesLog, sensitiveAttribute, clusterRelevantAttributes, k_clusters):
        # Make sure the sensitive attribute is last in line for later indexing
        if(sensitiveAttribute in clusterRelevantAttributes):
            clusterRelevantAttributes.remove(sensitiveAttribute)
        clusterRelevantAttributes.append(sensitiveAttribute)

        values = self._getEventAttributesTuples(xesLog, clusterRelevantAttributes)

        km = KModes(n_clusters=k_clusters, init='Huang', n_init=5)

        if(len(values[0]) == 1):
            values = np.array(values).reshape(-1, 1)

        clusters = km.fit_predict(values)
        valueClusterDict = self.__getValueToCluster(km, values)

        print(valueClusterDict)
        print(km.cluster_centroids_)

        # Apply clustered data mode to log
        for case_index, case in enumerate(xesLog):
            if(sensitiveAttribute in case.attributes.keys()):
                t = tuple((case.attributes[attribute] if attribute in case.attributes.keys() else 0) for attribute in clusterRelevantAttributes)
                case.attributes[sensitiveAttribute] = km.cluster_centroids_[valueClusterDict[t]][-1]

        return self.AddExtension(xesLog, 'con', 'case', sensitiveAttribute)

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

    def __getValueToCluster(self, kmeans, values):
        # Provides a cluster number for every key
        valueClusterDict = {}
        for i in range(len(kmeans.labels_)):
            if values[i] not in valueClusterDict:
                valueClusterDict[values[i]] = kmeans.labels_[i]
        return valueClusterDict

    def __getClusterMode(self, kmeans, values):
        valueClusterDict = self.__getValueToCluster(kmeans, values)

        clusterMode = {}
        for i in range(kmeans.n_clusters):
            clusterMode[i] = self.__getMode([x for x in valueClusterDict.keys() if valueClusterDict[x] == i])

        return clusterMode
