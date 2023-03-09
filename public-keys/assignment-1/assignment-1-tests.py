
# Imports for test cases
import unittest
import requests
import json

# Overall structure of the test case. Will differ in terms of structure and how they are run in groups while actual grading.


class testAPIs(unittest.TestCase):
    baseURL = "http://127.0.0.1:5050"
    currentResult = None  # holds last result object passed to run method

    def testCase1(self):
        # Test case 1 (weight 16)
        testCase = requests.post(self.baseURL + "/message", json={
                                 "data": {"command": None, "message": "alert this has no command"}})
        self.assertEqual(json.loads(testCase.content.decode()), {
            "data": {"command": None, "message": "alert this has no command"}}
        )

    def testCase2(self):
        # Test case 2 (weight 15.5)
        testCase = requests.post(self.baseURL + "/message", json={
                                 "data": {"command": None, "message": "alert /this has no command"}})
        self.assertEqual(json.loads(testCase.content.decode()), {
            "data": {"command": None, "message": "alert /this has no command"}}
        )

    def testCase3(self):
        # Test case 3 (weight 15.5)
        testCase = requests.post(self.baseURL + "/message", json={
                                 "data": {"command": None, "message": "a/lert this has no command"}})
        self.assertEqual(json.loads(testCase.content.decode()), {
            "data": {"command": None, "message": "a/lert this has no command"}}
        )

    def testCase4(self):
        # Test case 4 (weight 16)
        testCase = requests.post(self.baseURL + "/message", json={
                                 "data": {"command": None, "message": "/alert this has an alert command"}})
        self.assertEqual(json.loads(testCase.content.decode()), {
            "data": {"command": "alert", "message": "this has an alert command"}}
        )

    def testCase5(self):
        # Test case 5 (weight 16)
        testCase = requests.post(self.baseURL + "/message", json={
                                 "data": {"command": None, "message": "/reminder/ this is a reminder"}})
        self.assertEqual(json.loads(testCase.content.decode()), {
            "data": {"command": "reminder/", "message": "this is a reminder"}}
        )

    def testCase6(self):
        # Test case 6 (weight 16)
        testCase = requests.post(self.baseURL + "/message", json={
                                 "data": {"command": None, "message": "/reminder /this is a reminder"}})
        self.assertEqual(json.loads(testCase.content.decode()), {
            "data": {"command": "reminder", "message": "/this is a reminder"}}
        )

    def testCase7(self):
        # Test case 7 (weight 1)
        testCase = requests.post(self.baseURL + "/message", json={
                                 "data": {"command": None, "message": "   /alert this has an alert command"}})
        self.assertEqual(json.loads(testCase.content.decode()), {
            "data": {"command": "alert", "message": "this has an alert command"}}
        )

    def testCase8(self):
        # Test case 8 (weight 1)
        testCase = requests.post(self.baseURL + "/message", json={
                                 "data": {"command": None, "message": "/alert"}})
        self.assertNotEqual(testCase.status_code, 200)
        self.assertNotEqual(testCase.status_code, 500)

    def testCase9(self):
        # Test case 9 (weight 1)
        testCase = requests.post(self.baseURL + "/message", json={
                                 "data": {"command": None, "message": "/ this is a message with no command"}})
        self.assertNotEqual(testCase.status_code, 200)
        self.assertNotEqual(testCase.status_code, 500)

    def testCase10(self):
        # Test case 10 (weight 1)
        testCase = requests.post(self.baseURL + "/message", json={
                                 "data": {"command": None, "message": ""}})
        self.assertNotEqual(testCase.status_code, 200)
        self.assertNotEqual(testCase.status_code, 500)

    def testCase11(self):
        # Test case 1 (weight 1)
        testCase = requests.post(self.baseURL + "/message", json={
                                 "data": {"command": None, "message": "/alert this has an alert command    "}})
        self.assertEqual(json.loads(testCase.content.decode()), {
            "data": {"command": "alert", "message": "this has an alert command"}}
        )

    def test_all_cases(self):
        # Define the weights of each test
        test_weights = {
            self.testCase1: 16,
            self.testCase2: 15.5,
            self.testCase3: 15.5,
            self.testCase4: 16,
            self.testCase5: 16,
            self.testCase6: 16,
            self.testCase7: 1,
            self.testCase8: 1,
            self.testCase9: 1,
            self.testCase10: 1,
            self.testCase11: 1
        }
        # Run all test cases and calculate the total value based on the number of passed tests and their weights
        passed_tests = [t for t in [self.testCase1,
                                    self.testCase2, self.testCase3, self.testCase4,
                                    self.testCase5, self.testCase6, self.testCase7,
                                    self.testCase8, self.testCase9, self.testCase10, self.testCase11] if self.run_test(t)]
        total_value = sum([test_weights[t] for t in passed_tests])
        # Print the total value
        print("Total value:", total_value)

    def run_test(self, test):
        # Helper function to run a single test and return True if it passed or False if it failed
        try:
            test()
            return True
        except AssertionError:
            return False


if __name__ == '__main__':
    unittest.main()
