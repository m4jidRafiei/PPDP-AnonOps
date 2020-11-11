from .anonymizationOperationInterface import AnonymizationOperationInterface
from pm4py.objects.log.importer.xes import factory as xes_importer_factory
import hashlib
from cryptography.fernet import Fernet
import base64


class Cryptography(AnonymizationOperationInterface):
    """Extract text from a PDF."""

    def __init__(self):
        super(Cryptography, self).__init__()
        self.cryptoKey = b'h3aDgKh3QwzTHBM3GRj4vYYuVD0zXWLMDjrxU3XUuQs='
        self.cryptoSalt = "a.9_Oq1S*23xLgB"

    def HashEventAttribute(self, xesLog, matchAttribute, matchAttributeValue, targetedAttribute, hashAlgo='ripemd160'):
        h = hashlib.new(hashAlgo)

        for case_index, case in enumerate(xesLog):
            for event_index, event in enumerate(case):
                if matchAttribute in event.keys():
                    if (event[matchAttribute] == matchAttributeValue):
                        # Only supress resource if activity value is a match
                        h.update(self.cryptoSalt + event[targetedAttribute].encode('utf-8'))
                        event[targetedAttribute] = h.hexdigest()

        self.AddExtension(xesLog, 'Cryptography', 'Event', targetedAttribute)

        return xesLog

    def EncryptEventAttribute(self, xesLog, matchAttribute, matchAttributeValue, targetedAttribute):
        cipher_suite = Fernet(self.cryptoKey)  # base64 coded 32-Byte key

        for case_index, case in enumerate(xesLog):
            for event_index, event in enumerate(case):
                if matchAttribute in event.keys():
                    if (event[matchAttribute] == matchAttributeValue):
                        # Only supress resource if activity value is a match
                        event[targetedAttribute] = base64.b64encode(cipher_suite.encrypt(event[targetedAttribute].encode('utf-8')))

        self.AddExtension(xesLog, 'Cryptography', 'Event', targetedAttribute)

        return xesLog

    def HashCaseAttribute(self, xesLog, matchAttribute, matchAttributeValue, targetedAttribute, hashAlgo='ripemd160'):
        h = hashlib.new(hashAlgo)

        for case_index, case in enumerate(xesLog):
            if matchAttribute in case.keys():
                if (case[matchAttribute] == matchAttributeValue):
                    # Only supress resource if activity value is a match
                    h.update(self.cryptoSalt + case[targetedAttribute].encode('utf-8'))
                    case[targetedAttribute] = h.hexdigest()

        self.AddExtension(xesLog, 'Cryptography', 'Case', targetedAttribute)

        return xesLog

    def EncryptCaseAttribute(self, xesLog, matchAttribute, matchAttributeValue, targetedAttribute):
        cipher_suite = Fernet(self.cryptoKey)  # base64 coded 32-Byte key

        for case_index, case in enumerate(xesLog):
            if matchAttribute in case.keys():
                if (case[matchAttribute] == matchAttributeValue):
                    # Only supress resource if activity value is a match
                    case[targetedAttribute] = base64.b64encode(cipher_suite.encrypt(case[targetedAttribute].encode('utf-8')))

        self.AddExtension(xesLog, 'Cryptography', 'Case', targetedAttribute)

        return xesLog
