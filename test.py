import unittest
from main import HTTPHeader
from test_cases import *


class TestHTTPParser(unittest.TestCase):
    def testMain(self):
        for i in range(len(test)):
            obj = HTTPHeader(test[i])
            obj.parse()
            self.assertEqual(exp[i], obj.output())

    def testDict(self):
        for i in range(len(test)):
            obj = HTTPHeader(test[i])
            obj.parse()
            self.assertEqual(expDict[i], obj.getHeaders())
