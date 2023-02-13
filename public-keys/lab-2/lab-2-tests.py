
# Imports for test cases
import unittest
import requests

# Overall structure of the test case. Will differ in terms of structure and how they are run in groups while actual grading.
class testAPIs(unittest.TestCase):
    baseURL = "http://127.0.0.1:5050"
    currentResult = None  # holds last result object passed to run method

    @classmethod
    def setResult(cls, amount, errors, failures, skipped):
        cls.amount, cls.errors, cls.failures, cls.skipped = \
            amount, errors, failures, skipped

    def tearDown(self):
        amount = self.currentResult.testsRun
        errors = self.currentResult.errors
        failures = self.currentResult.failures
        skipped = self.currentResult.skipped
        self.setResult(amount, errors, failures, skipped)

    @classmethod
    def tearDownClass(cls):
        print("\ntests run: " + str(cls.amount))
        print("errors: " + str(len(cls.errors)))
        print("failures: " + str(len(cls.failures)))
        print("success: " + str(cls.amount - len(cls.errors) - len(cls.failures)))
        print("skipped: " + str(len(cls.skipped)))

    def run(self, result=None):
        self.currentResult = result  # remember result for use in tearDown
        unittest.TestCase.run(self, result)  # call superclass run method

    def testAddAPI(self):
        with self.subTest():
            addCaseOne = requests.get(self.baseURL + "/add/1/4")
            self.assertEqual(float(addCaseOne.content.decode()), 5.0)
        with self.subTest():
            addCaseTwo = requests.get(self.baseURL + "/add/1.5/4.5")
            self.assertEqual(float(addCaseTwo.content.decode()), 6.0)
        with self.subTest():
            addCaseThree = requests.get(self.baseURL + "/add/-1/4.5")
            self.assertEqual(float(addCaseThree.content.decode()), 3.5)

    def testSubAPI(self):
        with self.subTest():
            subCaseOne = requests.get(self.baseURL + "/sub/4/1")
            self.assertEqual(float(subCaseOne.content.decode()), 3.0)
        with self.subTest():
            subCaseTwo = requests.get(self.baseURL + "/sub/1.5/4.5")
            self.assertEqual(float(subCaseTwo.content.decode()), -3.0)
        with self.subTest():
            subCaseThree = requests.get(self.baseURL + "/sub/10/2.5")
            self.assertEqual(float(subCaseThree.content.decode()), 7.5)

    def testMulAPI(self):
        with self.subTest():
            mulCaseOne = requests.post(self.baseURL + "/mul/4/1")
            self.assertEqual(float(mulCaseOne.content.decode()), 4.0)
        with self.subTest():
            mulCaseTwo = requests.post(self.baseURL + "/mul/1.5/10")
            self.assertEqual(float(mulCaseTwo.content.decode()), 15.0)
        with self.subTest():
            mulCaseThree = requests.post(self.baseURL + "/mul/-1/2.5")
            self.assertEqual(float(mulCaseThree.content.decode()), -2.5)

    def testDivAPI(self):
        with self.subTest():
            divCaseOne = requests.post(self.baseURL + "/div/4/1")
            self.assertEqual(float(divCaseOne.content.decode()), 4.0)
        with self.subTest():
            divCaseTwo = requests.post(self.baseURL + "/div/1.5/-10")
            self.assertEqual(float(divCaseTwo.content.decode()), -0.15)
        with self.subTest():
            divCaseThree = requests.post(self.baseURL + "/div/0/2.5")
            self.assertEqual(float(divCaseThree.content.decode()), 0.0)
        with self.subTest():
            divCaseThree = requests.post(self.baseURL + "/div/0/0")
            self.assertNotEqual(divCaseThree.status_code, 200) # In case your API returns a 200 with an error string, this test case would be excused as it will fail.

if __name__ == '__main__':
    unittest.main()
