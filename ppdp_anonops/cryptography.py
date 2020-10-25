from ppdp_anonops.anonymizationOperationInterface import anonymizationOperationInterface
from pm4py.objects.log.importer.xes import factory as xes_importer_factory
import hashlib
from cryptography.fernet import Fernet
import base64


class cryptography(anonymizationOperationInterface):
    """Extract text from a PDF."""

    def __init__(self, xesLogPath):
        super(cryptography, self).__init__(xesLogPath)
        self.cryptoKey = b'h3aDgKh3QwzTHBM3GRj4vYYuVD0zXWLMDjrxU3XUuQs='
        self.cryptoSalt = "a.9_Oq1S*23xLgB"

    def hashEventAttribute(self, matchAttribute, matchAttributeValue, targetedAttribute):
        h = hashlib.new('ripemd160')

        for case_index, case in enumerate(self.xesLog):
            for event_index, event in enumerate(case):
                if (event[matchAttribute] == matchAttributeValue):
                    # Only supress resource if activity value is a match
                    h.update(self.cryptoSalt + event[targetedAttribute].encode('utf-8'))
                    event[targetedAttribute] = h.hexdigest()

        self.AddExtension('Cryptography', 'Event', targetedAttribute)

    def encryptEventAttribute(self, matchAttribute, matchAttributeValue, targetedAttribute):
        cipher_suite = Fernet(self.cryptoKey)  # base64 coded 32-Byte key

        for case_index, case in enumerate(self.xesLog):
            for event_index, event in enumerate(case):
                if (event[matchAttribute] == matchAttributeValue):
                    # Only supress resource if activity value is a match
                    event[targetedAttribute] = base64.b64encode(cipher_suite.encrypt(event[targetedAttribute].encode('utf-8')))

        self.AddExtension('Cryptography', 'Event', targetedAttribute)
