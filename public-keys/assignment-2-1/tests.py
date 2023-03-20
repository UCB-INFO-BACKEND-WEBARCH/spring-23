
# Imports for test cases
import unittest
import requests
import json

# Overall structure of the test case. Will differ in terms of structure and how they are run in groups while actual grading.


class testAPIs(unittest.TestCase):
    baseURL = "http://127.0.0.1:5050"
    shrugURL = "http://127.0.0.1:5051"
    currentResult = None  # holds last result object passed to run method

    # Checking that the old code (command without a server) still works like Assignment 1
    def testCase1(self):
        # Test case 1 (weight: 10)
        with open("serverMapping.json", "w") as f:
            json.dump({}, f)
            f.close()
        testCase = requests.post(self.baseURL + "/message", json={
                                 "data": {"command": None, "message": "/shrug no shrug expected"}})
        responseMessage = json.loads(testCase.content.decode())[
            'data']['message']
        self.assertEqual(responseMessage, "no shrug expected")

    # Test case that adds the sever mapping to the file and
    # then calls the /message endpoint for that command
    def testCase2(self):
        # Test case 2 (weight: 30)
        with open("serverMapping.json", "w") as f:
            json.dump({"shrug": "http://localhost:5051"}, f)
            f.close()
        testCase = requests.post(self.baseURL + "/message", json={
                                 "data": {"command": None, "message": "/shrug no shrug expected"}})
        if testCase.ok:
            responseMessage = json.loads(testCase.content.decode())[
                'data']['message']
            self.assertNotEqual(responseMessage, "no shrug expected")
            self.assertTrue("no shrug expected" in responseMessage)
            self.assertTrue("¯\_(ツ)_/¯" in responseMessage)
        else:
            with open("serverMapping.json", "w") as f:
                json.dump({"shrug": "http://localhost:5051/"}, f)
                f.close()
            testCase = requests.post(self.baseURL + "/message", json={
                "data": {"command": None, "message": "/shrug no shrug expected"}})
            responseMessage = json.loads(testCase.content.decode())[
                'data']['message']
            self.assertNotEqual(responseMessage, "no shrug expected")
            self.assertTrue("no shrug expected" in responseMessage)
            self.assertTrue("¯\_(ツ)_/¯" in responseMessage)

    # Test case that uses the /register endpoint and checks that the serverMapping.json was updated
    # Then calls the /message endpoint for that command
    def testCase3(self):
        # Test case 3 (weight: 30)
        with open("serverMapping.json", "w") as f:
            json.dump({}, f)
            f.close()
        requests.post(self.baseURL + "/register", json={
            "data": {"command": "shrug", "server_url": self.shrugURL}})
        file = open('serverMapping.json')
        data = json.load(file)
        file.close()
        self.assertNotEqual(data, {})
        testCase = requests.post(self.baseURL + "/message", json={
                                 "data": {"command": "shrug", "message": "/shrug no shrug expected"}})
        responseMessage = json.loads(testCase.content.decode())[
            'data']['message']
        self.assertNotEqual(responseMessage, "no shrug expected")
        self.assertTrue("no shrug expected" in responseMessage)
        self.assertTrue("¯\_(ツ)_/¯" in responseMessage)

    # Test case that checks the edge case by directly calling the execute function in shrug server
    # Passes the wrong command and checks if the call fails (returns some kind of error)
    def testCase4(self):
        # Test case 4 (weight: 5)
        testCase = requests.post(self.shrugURL + "/execute", json={
                                 "data": {"command": "notShrug", "message": "this is a message"}})
        self.assertTrue(not testCase.ok)
        self.assertNotEqual(testCase.status_code, 200)
        self.assertNotEqual(testCase.status_code, 500)
        self.assertNotEqual(testCase.status_code, 201)

    # Test case that directly calls the /execute endpoint for Shrug Server with the right parameters
    # Expects to pass
    def testCase5(self):
        # Test case 5 (weight: 20)
        testCase = requests.post(
            self.shrugURL + "/execute", json={"data": {"command": "shrug", "message": "this is a message"}})
        responseMessage = json.loads(testCase.content.decode())[
            'data']['message']
        self.assertTrue("this is a message" in responseMessage)
        self.assertTrue("¯\_(ツ)_/¯" in responseMessage)

    # Test case that ensures that the /register endpoint should fail with the wrong inputs
    def testCase6(self):
        # Test case 6 (weight: 5)
        testCase = requests.post(
            self.baseURL + "/register", json={"data": {"command": None}})
        self.assertTrue(not testCase.ok)
        self.assertNotEqual(testCase.status_code, 200)
        self.assertNotEqual(testCase.status_code, 500)
        self.assertNotEqual(testCase.status_code, 201)

    def test_all_cases(self):
        # Define the weights of each test
        test_weights = {
            self.testCase1: 10,
            self.testCase2: 30,
            self.testCase3: 30,
            self.testCase4: 5,
            self.testCase5: 20,
            self.testCase6: 5
        }
        # Run all test cases and calculate the total value based on the number of passed tests and their weights
        passed_tests = [t for t in [self.testCase1, self.testCase2,
                                    self.testCase3, self.testCase4,
                                    self.testCase5, self.testCase6]
                        if self.run_test(t)]
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
