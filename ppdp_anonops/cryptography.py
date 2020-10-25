from anonymizationOperations import anonymizationOperationInterface
from pm4py.objects.log.importer.xes import factory as xes_importer_factory
import hashlib
from cryptography.fernet import Fernet
import base64

class Cryptography_AO(anonymizationOperationInterface):
    """Extract text from a PDF."""

    def __init__(self):
        #self.name = name
        # d = list(hashlib.algorithms_guaranteed)
        # d.sort()
        pass

    def Process(self, xes_path: str, parameter) -> str:
        xes_log = xes_importer_factory.apply(xes_path)
        no_traces = len(xes_log)
        no_events = sum([len(trace) for trace in xes_log])


    def hashEventAttribute(self, xes_log):
        refActivity = "concept:name"
        refActivityValue = "decide"
        targetedAttribute = "org:resource"

        h = hashlib.new('ripemd160')

        for case_index, case in enumerate(xes_log):
            for event_index, event in enumerate(case):
                if (event[refActivity] == refActivityValue):
                    #Only supress resource if activity value is a match
                    h.update(event[targetedAttribute].encode('utf-8'))
                    event[targetedAttribute] = h.hexdigest()

        return {'Operation': 'Cryptography', 'Result': result}
        pass

    def encryptEventAttribute(self, xes_log):
        refActivity = "concept:name"
        refActivityValue = "decide"
        targetedAttribute = "org:resource"



        cipher_suite = Fernet(b'h3aDgKh3QwzTHBM3GRj4vYYuVD0zXWLMDjrxU3XUuQs=') #base64 coded 32-Byte key
        cipher_text = cipher_suite.encrypt(b"A really secret message. Not for prying eyes.")
        #plain_text = cipher_suite.decrypt(cipher_text)


        for case_index, case in enumerate(xes_log):
            for event_index, event in enumerate(case):
                if (event[refActivity] == refActivityValue):
                    #Only supress resource if activity value is a match
                    event[targetedAttribute] = base64.b64encode(cipher_suite.encrypt(event[targetedAttribute].encode('utf-8')))


        return {'Operation': 'Cryptography', 'Result': result}
        pass
