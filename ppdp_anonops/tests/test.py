
from pm4py.objects.log.importer.xes import factory as xes_importer_factory
from pm4py.objects.log.exporter.xes import factory as xes_exporter
import hashlib
from cryptography.fernet import Fernet
from ppdp_anonops import Condensation, Swapping, Addition
import base64
from math import sqrt
from ppdp_anonops.utils import *

# running_example.xes
# Traces: 6
# Events 42
import numpy as np
from kmodes.kmodes import KModes


def main():
    tax = TaxonomyTree()
    n_healthcare = tax.AddNode("Healthcare")

    n_hospital = n_healthcare.AddChildNode("Hospital")
    n_surgery = n_hospital.AddChildNode("Surgery")
    n_surgery.AddChildNode("Surgeon")
    n_surgery.AddChildNode("Anesthesist")
    n_surgery.AddChildNode("Caretaker")
    n_diagnostic = n_hospital.AddChildNode("Diagnostic")
    n_diagnostic.AddChildNode("Internist")
    n_diagnostic.AddChildNode("Pharmacist")
    n_diagnostic.AddChildNode("Caretaker")

    n_insurance = n_healthcare.AddChildNode("Insurance")
    n_insurance.AddChildNode("Bookkeeping")
    n_insurance.AddChildNode("IT")
    n_insurance.AddChildNode("Consulting")
    n_insurance.AddChildNode("Support")

    n_aerospace = tax.AddNode("Aerospace")
    n_it = tax.AddNode("IT")

    tax.PrintTree()
    print('\n\n')
    dict = tax.GetGeneralizedDict_NodeNameToDepthXParentalName(2)
    print(dict)
    print('\n\n')
    dict = tax.GetGeneralizedDict_NodeNameToDepthXParentalName(3)
    print(dict)
    print('\n\n')
    dict = tax.GetGeneralizedDict_NodeNameToDepthXParentalName(4)
    print(dict)
    print('\n\n')

    a = Addition('resources/running_example.xes')
    print(type(a.xesLog))

# def euclidianDistance(weights, attributesA, attributesB):
#     if(len(weights) != len(attributesA) != len(attributesB)):
#         # raise

#     sum = 0

#     for i in range(len(weights)):
#         sum += weights[i] * ((attributesA[i] - attributesB[i]) ** 2)

#     return sqrt(sum)


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
