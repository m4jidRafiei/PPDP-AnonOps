from unittest import TestCase
import os
from ppdp_anonops import Cryptography
from pm4py.objects.log.importer.xes import factory as xes_importer


class TestCryptography(TestCase):
    def getTestXesLog(self):
        xesPath = os.path.join(os.path.dirname(__file__), 'resources', 'running_example.xes')
        return xes_importer.apply(xesPath)
