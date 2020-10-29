from unittest import TestCase
import os
from ppdp_anonops.cryptography import cryptography


class TestCryptography(TestCase):
    def getTestXesPath(self):
        return os.path.join(os.path.dirname(__file__), 'resources', 'running_example.xes')