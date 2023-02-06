"""
Write a Python Function that takes in an integer input (say 129) and returns a string that names each digit separately ("one two nine").

To get a Check+ (10/10) - Your function should have passed the first five test cases and failed the next two!

Also feel free to play with the last test case if you are using Error/Exception Handling as part of your function.
"""

# Response Type 1 - Using conditionals

# def numToString(num):
#     # Handling errors with input
#     if type(num) is not int or num < 0:
#         raise Exception("Invalid Input")
#     num_str = str(num)
#     output = ""
#     for i in num_str:
#         if i == "0":
#             output += ' ' + 'zero'
#         elif i == "1":
#             output += ' ' + 'one'
#         elif i == "2":
#             output += ' ' + 'two'
#         elif i == "3":
#             output += ' ' + 'three'
#         elif i == "4":
#             output += ' ' + 'four'
#         elif i == "5":
#             output += ' ' + 'five'
#         elif i == "6":
#             output += ' ' + 'six'
#         elif i == "7":
#             output += ' ' + 'seven'
#         elif i == "8":
#             output += ' ' + 'eight'
#         elif i == "9":
#             output += ' ' + 'nine'
#     output = output[1:]
#     return output


# Response Type 2 - Using a dictionary

# def numToString(num):
#     # Handling errors with input
#     if type(num) is not int or num < 0:
#         raise Exception("Invalid Input")
#     digit_names = {
#         0: "zero",
#         1: "one",
#         2: "two",
#         3: "three",
#         4: "four",
#         5: "five",
#         6: "six",
#         7: "seven",
#         8: "eight",
#         9: "nine"
#     }
#     num_str = str(num)
#     result = [digit_names[int(digit)] for digit in num_str]
#     return " ".join(result)

# Response Type 3 - Using an array

# def numToString(num: int):
#     # Handling errors with input
#     if type(num) is not int or num < 0:
#         raise Exception("Invalid Input")

#     digit_names = [
#         "zero", "one", "two", "three", "four",
#         "five", "six", "seven", "eight", "nine"
#     ]
#     while input >= 0:
#         pass
#         if input == 0:
#             break
#     num_str = str(num)
#     result = [digit_names[int(digit)] for digit in num_str]
#     # Can also use strip/splice at the end to remove spaces if not using join function
#     return " ".join(result)

# Response Type 4 - Using dictionary but looping without conversion input to string

def numToString(num):
    # Handling errors with input
    if type(num) is not int or num < 0:
        raise Exception("Invalid Input")
    output = ""
    nums_letters = {0: 'zero', 1: 'one', 2: 'two', 3: 'three', 4: 'four', 5:
                    'five', 6: 'six', 7: 'seven', 8: 'eight', 9: 'nine'}
    while num >= 0:
        digit = num % 10
        if output == "":
            output = nums_letters[digit]
        else:
            output = nums_letters[digit] + ' ' + output
        num = num // 10
        if num == 0:
            break
    return output


# Test cases for Lab 1
def testNumToString():

    # The below test cases should pass
    # Test Case 1 - Should pass
    assert numToString(129) == "one two nine"
    # Test Case 2 - Should pass
    assert numToString(0) == "zero"
    # Test Case 3 - Should pass
    assert numToString(1001) == "one zero zero one"
    # Test Case 4 - Should pass
    assert numToString(
        123456789) == "one two three four five six seven eight nine"
    # Test Case 5 - Should pass
    assert numToString(111) == "one one one"

    # The next two test cases should essentially fail as your function should only accept ints and reject everything else
    # Test Case 6 - Should fail
    assert numToString("129") == "one two nine"
    # Test Case 7 - Should fail
    assert numToString("009") == "nine"

    # Test case that will check for exactly your Exception
    # In this case, it is listening to an exception that says "Invalid Input"
    # You can comment it or change it to match your code!
    # try:
    #     numToString("129")
    # except Exception as error:
    #     assert str(error) == "Invalid Input"
    # else:
    #     assert False, "Expected a TypeError to be raised"


testNumToString()
