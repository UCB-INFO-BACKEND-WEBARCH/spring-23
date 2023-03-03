
# Imports for test cases
import unittest
import requests
import json

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
        # print("\ntests run: " + str(cls.amount))
        # print("errors: " + str(len(cls.errors)))
        # print("failures: " + str(len(cls.failures)))
        # print("success: " + str(cls.amount - len(cls.errors) - len(cls.failures)))
        # print("skipped: " + str(len(cls.skipped)))
        if cls.amount - len(cls.errors) - len(cls.failures) >= 8:
            print("10/10")
        elif cls.amount - len(cls.errors) - len(cls.failures) >= 6:
            print("8.5/10")
        elif cls.amount - len(cls.errors) - len(cls.failures) >= 4:
            print("7/10")
        else:
            print("0/10")

    def run(self, result=None):
        self.currentResult = result  # remember result for use in tearDown
        unittest.TestCase.run(self, result)  # call superclass run method

    # Get all with no content - 204
    def testOne(self):
        with open("quotes.json", "w") as f:
            json.dump({}, f)
            f.close()
        testCase = requests.get(self.baseURL + "/")
        self.assertEqual(testCase.status_code, 204)

    # POST call with right format - 201
    def testTwo(self):
        with open("quotes.json", "w") as f:
            json.dump({}, f)
            f.close()
        testCase = requests.post(self.baseURL + "/", json={"day": "sunday",
                                                           "quote": "Before you date someone, make them use a computer with slow internet to see who they really are"})
        self.assertEqual(json.loads(testCase.content.decode()), {
            "sunday": "Before you date someone, make them use a computer with slow internet to see who they really are"})
        self.assertEqual(testCase.status_code, 201)

    # POST call with wrong format - 400
    def testThree(self):
        with open("quotes.json", "w") as f:
            json.dump({}, f)
            f.close()
        testCase = requests.post(self.baseURL + "/", json={"day": "munday",
                                                           "quote": "This should give a 400 :/"})
        self.assertEqual(testCase.status_code, 400)

    # Get by Day with wrong day - 400
    def testFour(self):
        with open("quotes.json", "w") as f:
            json.dump({}, f)
            f.close()
        testCase = requests.get(self.baseURL + "/munday")
        self.assertEqual(testCase.status_code, 400)

    # Get All - 200
    def testFive(self):
        with open("quotes.json", "w") as f:
            json.dump({
                "sunday": "Before you date someone, make them use a computer with slow internet to see who they really are"}, f)
            f.close()
        with self.subTest():
            testCase = requests.get(self.baseURL + "/")
            self.assertEqual(json.loads(testCase.content.decode()), {
                "sunday": "Before you date someone, make them use a computer with slow internet to see who they really are"})

    # Get by Day - 200
    def testSix(self):
        with open("quotes.json", "w") as f:
            json.dump({
                "sunday": "Before you date someone, make them use a computer with slow internet to see who they really are"}, f)
            f.close()
        with self.subTest():
            testCase = requests.get(self.baseURL + "/sunday")
            self.assertEqual(json.loads(testCase.content.decode()), {
                "sunday": "Before you date someone, make them use a computer with slow internet to see who they really are"})

    # Edit an existing key - 200
    def testSeven(self):
        with open("quotes.json", "w") as f:
            json.dump({
                "sunday": "Before you date someone, make them use a computer with slow internet to see who they really are"}, f)
            f.close()
        testCase = requests.put(
            self.baseURL + "/sunday", json={"quote": "I love mankind... it's people I can't stand!"})
        self.assertEqual(testCase.status_code, 200)
        self.assertEqual(json.loads(testCase.content.decode()), {
            "sunday": "I love mankind... it's people I can't stand!"})

    # Edit a new key - 201
    def testEight(self):
        with open("quotes.json", "w") as f:
            json.dump({
            }, f)
            f.close()
        testCase = requests.put(
            self.baseURL + "/monday", json={"quote": "New sunday quote"})
        self.assertEqual(testCase.status_code, 201)
        self.assertEqual(json.loads(testCase.content.decode()), {
            "monday": "New sunday quote"})

    # Delete a day - 200
    def testNine(self):
        with open("quotes.json", "w") as f:
            json.dump({
                "sunday": "I love mankind... it's people I can't stand!", "monday": "Before you date someone, make them use a computer with slow internet to see who they really are"}, f)
            f.close()
        testCase = requests.delete(
            self.baseURL + "/sunday")
        self.assertEqual(testCase.status_code, 200)

    # Delete a day - 404
    def testTen(self):
        with open("quotes.json", "w") as f:
            json.dump({}, f)
            f.close()
        testCase = requests.delete(
            self.baseURL + "/sunday")
        self.assertEqual(testCase.status_code, 404)


if __name__ == '__main__':
    unittest.main()
