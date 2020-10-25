
# from pm4py.objects.log.importer.xes import factory as xes_importer_factory
# from pm4py.objects.log.exporter.xes import factory as xes_exporter
# import hashlib
# from cryptography.fernet import Fernet
# import base64
# #running_example.xes
# #Traces: 6
# #Events 42


# def main():
#     xes_log = xes_importer_factory.apply("resources/running_example.xes")
#     print("no_traces = " + str(len(xes_log)))
#     print("no_events = " + str(sum([len(trace) for trace in xes_log])))

#     case_attribs, event_attribs = getAttr(xes_log)
#     print(*case_attribs, sep = ", ")
#     print(*event_attribs, sep = ", ")

#     print("\n\napplying...\n\n")


#     refActivity = "concept:name"
#     refActivityValue = "decide"
#     targetedAttribute = "org:resource"

#     cipher_suite = Fernet(b'h3aDgKh3QwzTHBM3GRj4vYYuVD0zXWLMDjrxU3XUuQs=') #base64 coded 32-Byte key
#     cipher_text = cipher_suite.encrypt(b"A really secret message. Not for prying eyes.")
#     #plain_text = cipher_suite.decrypt(cipher_text)


#     for case_index, case in enumerate(xes_log):
#         for event_index, event in enumerate(case):
#             if (event[refActivity] == refActivityValue):
#                 #Only supress resource if activity value is a match
#                 event[targetedAttribute] = base64.b64encode(cipher_suite.encrypt(event[targetedAttribute].encode('utf-8')))


#     print("no_traces = " + str(len(xes_log)))
#     print("no_events = " + str(sum([len(trace) for trace in xes_log])))

#     xes_exporter.export_log(xes_log, "exportedLog.xes")


# def getAttr(xes_log):
#     case_attribs = []
#     for case_index, case in enumerate(xes_log):
#         for key in case.attributes.keys():
#             if key not in case_attribs:
#                 case_attribs.append(key)
#     event_attribs = []
#     for case_index, case in enumerate(xes_log):
#         for event_index, event in enumerate(case):
#             for key in event.keys():
#                 if key not in event_attribs:
#                     event_attribs.append(key)
#     return case_attribs, event_attribs

# if __name__ == "__main__":
#     main()
